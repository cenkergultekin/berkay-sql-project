"""
Route handlers for SQL Agent application.
Separated route logic from main application.
"""
from flask import Blueprint, request, jsonify, session
from typing import Dict, Any
import logging

from backend.models.models import DatabaseConnection, QueryRequest, SavedQuery
from backend.services.database import DatabaseManager
from backend.services.ai_service import AIService
from backend.core.utils import (
    ValidationError, SQLValidator, StringUtils,
    ResponseFormatter, LoggingUtils, ODBCUtils
)
from backend.config.config import Config
import keyring

logger = logging.getLogger(__name__)

# Create blueprint for routes
api_bp = Blueprint('api', __name__, url_prefix='/api')


class DatabaseRoutes:
    """Handles database-related routes."""
    
    def __init__(self):
        self.db_manager: DatabaseManager = None
        self.ai_service = AIService()
    
    def set_database_connection(self, connection_string: str, keyring_account: str | None = None) -> None:
        """Set database connection for the session.
        connection_string should NOT contain PWD.
        If keyring_account is provided, password will be retrieved from keyring at connect time.
        """
        try:
            # Validate connection string
            if not connection_string or not connection_string.strip():
                raise ValidationError("Connection string cannot be empty")
            
            # Create database manager
            self.db_manager = DatabaseManager(connection_string, keyring_account=keyring_account)
            
            # Test connection
            if not self.db_manager.test_connection():
                raise ValidationError("Database connection test failed")
            
            # Store in session
            session["DB_CONN_STR"] = connection_string  # sanitized (no PWD)
            if keyring_account:
                session["DB_KR_ACCOUNT"] = keyring_account
            logger.info("Database connection established successfully (credentials stored securely)")
            
        except Exception as e:
            logger.error(f"Failed to set database connection: {e}")
            raise
    
    def get_database_manager(self) -> DatabaseManager:
        """Get database manager instance."""
        if not self.db_manager:
            connection_string = session.get("DB_CONN_STR")
            if not connection_string:
                raise ValidationError("No database connection found. Please set database connection first.")
            keyring_account = session.get("DB_KR_ACCOUNT")
            self.db_manager = DatabaseManager(connection_string, keyring_account=keyring_account)
        return self.db_manager

    def clear_connection(self) -> None:
        """Clear stored credentials and session."""
        try:
            keyring_account = session.pop("DB_KR_ACCOUNT", None)
            session.pop("DB_CONN_STR", None)
            if keyring_account:
                try:
                    keyring.delete_password(Config.KEYRING_SERVICE, keyring_account)
                except keyring.errors.PasswordDeleteError:
                    pass
            self.db_manager = None
            logger.info("Database connection info cleared from keyring/session")
        except Exception as e:
            logger.error(f"Failed to clear connection info: {e}")
            raise


# Global routes instance
db_routes = DatabaseRoutes()


@api_bp.route("/set_db", methods=["POST"])
def set_database():
    """Set database connection securely.
    Accepts either:
      - { db_conn_str: "DRIVER=...;SERVER=...;DATABASE=...;UID=...;PWD=..." }
      - { driver, server, database, uid, pwd }
    Stores password in OS Keyring, saves DSN without PWD in session.
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify(ResponseFormatter.format_error_response("No data provided")), 400
        
        # Case 1: full DSN provided
        connection_string = data.get("db_conn_str")
        driver = data.get("driver")
        server = data.get("server")
        database_name = data.get("database")
        uid = data.get("uid") or data.get("username")
        pwd = data.get("pwd") or data.get("password")

        keyring_account = None
        dsn_without_pwd = None

        if connection_string:
            # Sanitize input
            connection_string = StringUtils.sanitize_input(connection_string, 2000)
            parsed = ODBCUtils.parse_dsn(connection_string)
            # Extract values
            driver_val = parsed.get("DRIVER") or f"{{{Config.DEFAULT_ODBC_DRIVER}}}"
            server_val = parsed.get("SERVER")
            db_val = parsed.get("DATABASE")
            uid_val = parsed.get("UID")
            pwd_val = parsed.get("PWD")
            if not (server_val and db_val and uid_val and pwd_val):
                return jsonify(ResponseFormatter.format_error_response("Invalid connection string. Required keys: SERVER, DATABASE, UID, PWD")), 400
            # Build DSN without password for storage
            dsn_without_pwd = ODBCUtils.build_dsn(driver_val.strip("{}"), server_val, db_val, uid_val, None)
            # Store password to keyring
            keyring_account = f"{server_val}|{db_val}|{uid_val}"
            keyring.set_password(Config.KEYRING_SERVICE, keyring_account, pwd_val)
        else:
            # Case 2: fields provided
            driver_val = (driver or Config.DEFAULT_ODBC_DRIVER)
            server_val = (server or "").strip()
            db_val = (database_name or "").strip()
            uid_val = (uid or "").strip()
            pwd_val = (pwd or "").strip()
            if not (server_val and db_val and uid_val and pwd_val):
                return jsonify(ResponseFormatter.format_error_response("Missing required fields: server, database, uid, pwd")), 400
            dsn_without_pwd = ODBCUtils.build_dsn(driver_val, server_val, db_val, uid_val, None)
            keyring_account = f"{server_val}|{db_val}|{uid_val}"
            keyring.set_password(Config.KEYRING_SERVICE, keyring_account, pwd_val)

        # Log masked DSN only
        logger.info(f"Setting DB connection with DSN: {ODBCUtils.mask_dsn(dsn_without_pwd)}")

        # Set database connection (will fetch pwd from keyring)
        db_routes.set_database_connection(dsn_without_pwd, keyring_account=keyring_account)
        
        
        return jsonify(ResponseFormatter.format_success_response(
            None, 
            "Veritabanı bağlantısı başarıyla kuruldu."
        ))
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error setting database: {e}")
        return jsonify(ResponseFormatter.format_error_response("Database connection failed")), 500


@api_bp.route("/clear_db", methods=["POST"])
def clear_database_credentials():
    """Remove stored DB credentials from keyring and clear session."""
    try:
        db_routes.clear_connection()
        # Optionally stop scheduler jobs that depend on DB; we'll leave scheduler running but without DB it won't execute
        return jsonify(ResponseFormatter.format_success_response(None, "Bağlantı bilgileri temizlendi."))
    except Exception as e:
        logger.error(f"Error clearing database credentials: {e}")
        return jsonify(ResponseFormatter.format_error_response("Bağlantı bilgileri temizlenemedi")), 500


@api_bp.route("/tables", methods=["GET"])
def get_tables():
    """Get list of all tables in the database."""
    try:
        db_manager = db_routes.get_database_manager()
        tables = db_manager.get_tables()
        
        return jsonify(ResponseFormatter.format_success_response(tables))
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error getting tables: {e}")
        return jsonify(ResponseFormatter.format_error_response("Failed to retrieve tables")), 500


@api_bp.route("/columns", methods=["POST"])
def get_columns():
    """Get columns for specified tables."""
    try:
        data = request.get_json()
        if not data:
            return jsonify(ResponseFormatter.format_error_response("No data provided")), 400
        
        tables = data.get("tables", [])
        if not tables:
            return jsonify(ResponseFormatter.format_error_response("No tables specified")), 400
        
        # Validate table names
        if len(tables) > Config.MAX_TABLES_PER_QUERY:
            return jsonify(ResponseFormatter.format_error_response(
                f"Too many tables specified. Maximum allowed: {Config.MAX_TABLES_PER_QUERY}"
            )), 400
        
        # Sanitize table names
        tables = [StringUtils.sanitize_input(table) for table in tables]
        
        db_manager = db_routes.get_database_manager()
        columns_dict = db_manager.get_multiple_table_columns(tables)
        
        return jsonify(ResponseFormatter.format_success_response(columns_dict))
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error getting columns: {e}")
        return jsonify(ResponseFormatter.format_error_response("Failed to retrieve columns")), 500


@api_bp.route("/query", methods=["POST"])
def execute_query():
    """Execute natural language query and return results."""
    try:
        data = request.get_json()
        if not data:
            return jsonify(ResponseFormatter.format_error_response("No data provided")), 400
        
        # Extract and validate request data
        question = data.get("question", "").strip()
        tables = data.get("tables", [])
        
        if not question:
            return jsonify(ResponseFormatter.format_error_response("Question is required")), 400
        
        if not tables:
            return jsonify(ResponseFormatter.format_error_response("At least one table must be specified")), 400
        
        # Sanitize inputs
        question = StringUtils.sanitize_input(question, Config.MAX_QUERY_LENGTH)
        tables = [StringUtils.sanitize_input(table) for table in tables]
        
        # Create query request
        query_request = QueryRequest(question=question, tables=tables)
        
        # Get database manager and schema
        db_manager = db_routes.get_database_manager()
        schema = db_manager.get_database_schema()
        
        # Convert natural language to SQL
        sql_query = db_routes.ai_service.convert_natural_to_sql(query_request, schema)
        
        # Validate generated SQL
        if not SQLValidator.validate_sql_query(sql_query):
            return jsonify(ResponseFormatter.format_error_response(
                "Generated SQL query is not valid or contains dangerous operations"
            )), 400
        
        # Execute query
        query_response = db_manager.execute_query(sql_query)
        
        # Save query to database with results
        saved_query = SavedQuery(
            question=question,
            sql_query=sql_query,
            tables_used=tables,
            is_successful=query_response.is_successful,
            error_message=query_response.error,
            query_results=query_response.results if query_response.is_select_query else None,
            result_message=query_response.message
        )
        query_id = db_manager.save_query(saved_query)
        
        # Save to text file for backup
        try:
            from datetime import datetime
            import os
            import pytz
            
            # Turkey timezone
            tz = pytz.timezone('Europe/Istanbul')
            
            backup_file = "sorgularim.txt"
            file_exists = os.path.exists(backup_file)
            
            with open(backup_file, 'a', encoding='utf-8') as f:
                if not file_exists:
                    f.write("=" * 80 + "\n")
                    f.write("SQL AGENT - SORGU GEÇMİŞİ\n")
                    f.write("=" * 80 + "\n\n")
                
                f.write("\n" + "=" * 80 + "\n")
                f.write(f"SORGU #{query_id if query_id else 'N/A'}\n")
                f.write(f"TARİH: {datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S %Z')}\n")
                f.write(f"DURUM: {'✅ BAŞARILI' if query_response.is_successful else '❌ HATA'}\n")
                f.write("=" * 80 + "\n\n")
                
                f.write(f"📝 SORU:\n{question}\n\n")
                
                f.write(f"📋 TABLOLAR:\n{', '.join(tables)}\n\n")
                
                f.write(f"🔍 SQL SORGUSU:\n{sql_query}\n\n")
                
                if query_response.is_successful:
                    if query_response.results:
                        f.write(f"📊 SONUÇLAR: {len(query_response.results)} satır\n")
                        if len(query_response.results) <= 5:
                            f.write(f"Veri: {query_response.results}\n")
                    elif query_response.message:
                        f.write(f"✅ MESAJ: {query_response.message}\n")
                else:
                    f.write(f"❌ HATA: {query_response.error}\n")
                
                f.write("\n")
            
            logger.info(f"Query backed up to {backup_file}")
        except Exception as e:
            logger.error(f"Error backing up query to file: {e}")
        
        # Add query ID to response
        formatted_response = ResponseFormatter.format_query_response(query_response)
        if query_id:
            formatted_response['query_id'] = query_id
        
        LoggingUtils.log_response_info("/query", query_response.is_successful, formatted_response)
        
        if query_response.is_successful:
            return jsonify(formatted_response)
        else:
            return jsonify(formatted_response), 400
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        return jsonify(ResponseFormatter.format_error_response("Query execution failed")), 500


@api_bp.route("/queries", methods=["GET"])
def get_saved_queries():
    """Get saved queries."""
    try:
        db_manager = db_routes.get_database_manager()
        
        # Get pagination parameters
        limit = request.args.get('limit', 50, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        # Validate parameters
        if limit > 100:
            limit = 100
        if offset < 0:
            offset = 0
        
        queries = db_manager.get_saved_queries(limit=limit, offset=offset)
        
        # Convert to dictionaries
        queries_data = [query.to_dict() for query in queries]
        
        return jsonify(ResponseFormatter.format_success_response(queries_data))
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error getting saved queries: {e}")
        return jsonify(ResponseFormatter.format_error_response("Failed to retrieve saved queries")), 500


@api_bp.route("/queries/<int:query_id>", methods=["DELETE"])
def delete_saved_query(query_id):
    """Delete a saved query."""
    try:
        db_manager = db_routes.get_database_manager()
        
        success = db_manager.delete_saved_query(query_id)
        
        if success:
            return jsonify(ResponseFormatter.format_success_response(
                None, 
                f"Sorgu #{query_id} başarıyla silindi."
            ))
        else:
            return jsonify(ResponseFormatter.format_error_response(
                f"Sorgu #{query_id} bulunamadı."
            )), 404
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error deleting query: {e}")
        return jsonify(ResponseFormatter.format_error_response("Failed to delete query")), 500


@api_bp.route("/queries/<int:query_id>", methods=["GET"])
def get_saved_query(query_id):
    """Get a specific saved query."""
    try:
        db_manager = db_routes.get_database_manager()
        
        query = db_manager.get_saved_query_by_id(query_id)
        
        if query:
            return jsonify(ResponseFormatter.format_success_response(query.to_dict()))
        else:
            return jsonify(ResponseFormatter.format_error_response(
                f"Sorgu #{query_id} bulunamadı."
            )), 404
        
    except ValidationError as e:
        return jsonify(ResponseFormatter.format_error_response(str(e))), 400
    except Exception as e:
        logger.error(f"Error getting query: {e}")
        return jsonify(ResponseFormatter.format_error_response("Failed to retrieve query")), 500


@api_bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    try:
        # Simple health check - just return that the service is running
        health_data = {
            "status": "healthy",
            "database_connected": False,  # Will be true when user connects
            "ai_service_available": True,
            "message": "SQL Agent is running"
        }
        
        return jsonify(ResponseFormatter.format_success_response(health_data))
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return jsonify(ResponseFormatter.format_error_response("Health check failed")), 500


# Create global instance
db_routes = DatabaseRoutes()

