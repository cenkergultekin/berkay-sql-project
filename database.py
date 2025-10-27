"""
Database operations and connection management.
Handles all database-related functionality.
"""
import pyodbc
from typing import List, Dict, Any, Optional
from contextlib import contextmanager
from models import DatabaseConnection, TableInfo, DatabaseSchema, QueryResponse, QueryType, SavedQuery
from config import Config
import logging
from utils import ODBCUtils
import keyring

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages database connections and operations."""
    
    def __init__(self, connection_string: str, keyring_account: Optional[str] = None):
        """Initialize database manager with sanitized connection string (no PWD).
        keyring_account identifies where the password is stored in OS keyring.
        """
        self.connection_string = connection_string
        self.keyring_account = keyring_account
        self.timeout = Config.DB_CONNECTION_TIMEOUT
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections."""
        conn = None
        try:
            # If keyring_account is set, fetch password and build full DSN
            dsn = self.connection_string
            if self.keyring_account:
                pwd = keyring.get_password(Config.KEYRING_SERVICE, self.keyring_account)
                if not pwd:
                    raise RuntimeError("Stored database password not found in keyring")
                parsed = ODBCUtils.parse_dsn(self.connection_string)
                driver_val = parsed.get("DRIVER") or f"{{{Config.DEFAULT_ODBC_DRIVER}}}"
                server_val = parsed.get("SERVER")
                db_val = parsed.get("DATABASE")
                uid_val = parsed.get("UID")
                if not (server_val and db_val and uid_val):
                    raise RuntimeError("Invalid stored DSN (missing SERVER/DATABASE/UID)")
                dsn = ODBCUtils.build_dsn(driver_val.strip("{}"), server_val, db_val, uid_val, pwd)

            conn = pyodbc.connect(
                dsn,
                timeout=self.timeout
            )
            yield conn
        except pyodbc.Error as e:
            logger.error(f"Database connection error: {e}")
            raise
        finally:
            if conn:
                conn.close()
    
    def test_connection(self) -> bool:
        """Test database connection."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT 1")
                cursor.fetchone()
            return True
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False
    
    def get_tables(self) -> List[str]:
        """Get list of all tables in the database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                    "WHERE TABLE_TYPE='BASE TABLE'"
                )
                tables = [row[0] for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(tables)} tables from database")
                return tables
        except Exception as e:
            logger.error(f"Error retrieving tables: {e}")
            raise
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get columns for a specific table."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS "
                    "WHERE TABLE_NAME = ?",
                    table_name
                )
                columns = [row[0] for row in cursor.fetchall()]
                logger.info(f"Retrieved {len(columns)} columns for table '{table_name}'")
                return columns
        except Exception as e:
            logger.error(f"Error retrieving columns for table '{table_name}': {e}")
            raise
    
    def get_multiple_table_columns(self, table_names: List[str]) -> Dict[str, List[str]]:
        """Get columns for multiple tables."""
        columns_dict = {}
        for table_name in table_names:
            try:
                columns_dict[table_name] = self.get_table_columns(table_name)
            except Exception as e:
                logger.error(f"Failed to get columns for table '{table_name}': {e}")
                raise
        return columns_dict
    
    def get_database_schema(self) -> DatabaseSchema:
        """Get complete database schema."""
        tables = self.get_tables()
        tables_info = {}
        
        for table_name in tables:
            columns = self.get_table_columns(table_name)
            tables_info[table_name] = TableInfo(name=table_name, columns=columns)
        
        return DatabaseSchema(tables=tables_info)
    
    def execute_query(self, sql_query: str) -> QueryResponse:
        """Execute SQL query and return results."""
        try:
            query_type = self._determine_query_type(sql_query)
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql_query)
                
                if query_type == QueryType.SELECT:
                    columns = [col[0] for col in cursor.description]
                    rows = cursor.fetchall()
                    results = [dict(zip(columns, row)) for row in rows]
                    
                    return QueryResponse(
                        sql_query=sql_query,
                        query_type=query_type,
                        results=results
                    )
                else:
                    conn.commit()
                    row_count = cursor.rowcount
                    
                    return QueryResponse(
                        sql_query=sql_query,
                        query_type=query_type,
                        message=f"{row_count} satır etkilendi.",
                        row_count=row_count
                    )
                    
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return QueryResponse(
                sql_query=sql_query,
                query_type=QueryType.OTHER,
                error=str(e)
            )
    
    def _determine_query_type(self, sql_query: str) -> QueryType:
        """Determine the type of SQL query."""
        query_upper = sql_query.strip().upper()
        
        if query_upper.startswith('SELECT'):
            return QueryType.SELECT
        elif query_upper.startswith('INSERT'):
            return QueryType.INSERT
        elif query_upper.startswith('UPDATE'):
            return QueryType.UPDATE
        elif query_upper.startswith('DELETE'):
            return QueryType.DELETE
        else:
            return QueryType.OTHER
    
    def create_queries_table(self) -> bool:
        """Create the saved_queries table if it doesn't exist."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Check if table exists
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM INFORMATION_SCHEMA.TABLES 
                    WHERE TABLE_NAME = 'saved_queries'
                """)
                
                if cursor.fetchone()[0] == 0:
                    # Create table
                    cursor.execute("""
                        CREATE TABLE saved_queries (
                            id INT IDENTITY(1,1) PRIMARY KEY,
                            question NVARCHAR(MAX) NOT NULL,
                            sql_query NVARCHAR(MAX) NOT NULL,
                            tables_used NVARCHAR(MAX),
                            created_at DATETIME2 DEFAULT GETDATE(),
                            is_successful BIT DEFAULT 1,
                            error_message NVARCHAR(MAX),
                            query_results NVARCHAR(MAX),
                            result_message NVARCHAR(MAX)
                        )
                    """)
                    conn.commit()
                    logger.info("Created saved_queries table")
                    return True
                else:
                    # Check if new columns exist, if not add them
                    cursor.execute("""
                        SELECT COUNT(*)
                        FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE TABLE_NAME = 'saved_queries' AND COLUMN_NAME = 'query_results'
                    """)
                    
                    if cursor.fetchone()[0] == 0:
                        cursor.execute("ALTER TABLE saved_queries ADD query_results NVARCHAR(MAX)")
                        cursor.execute("ALTER TABLE saved_queries ADD result_message NVARCHAR(MAX)")
                        conn.commit()
                        logger.info("Added query_results and result_message columns to saved_queries table")
                    
                    logger.info("saved_queries table already exists")
                    return True
                    
        except Exception as e:
            logger.error(f"Error creating queries table: {e}")
            return False
    
    def save_query(self, saved_query: SavedQuery) -> Optional[int]:
        """Save a query to the database."""
        try:
            import json
            from datetime import datetime, date
            from decimal import Decimal
            
            def json_serializer(obj):
                """JSON serializer for objects not serializable by default json code"""
                if isinstance(obj, (datetime, date)):
                    return obj.isoformat()
                if isinstance(obj, Decimal):
                    return float(obj)
                raise TypeError(f"Type {type(obj)} not serializable")
            
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Ensure table exists
                self.create_queries_table()
                
                # Convert query results to JSON string
                query_results_json = None
                if saved_query.query_results is not None:
                    query_results_json = json.dumps(saved_query.query_results, ensure_ascii=False, default=json_serializer)
                
                # Insert query
                cursor.execute("""
                    INSERT INTO saved_queries (question, sql_query, tables_used, is_successful, error_message, query_results, result_message)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    saved_query.question,
                    saved_query.sql_query,
                    ','.join(saved_query.tables_used) if saved_query.tables_used else '',
                    saved_query.is_successful,
                    saved_query.error_message,
                    query_results_json,
                    saved_query.result_message
                ))
                
                conn.commit()
                
                # Get the last inserted ID
                cursor.execute("SELECT @@IDENTITY")
                query_id = cursor.fetchone()[0]
                logger.info(f"Saved query with ID: {query_id}")
                return int(query_id) if query_id else None
                
        except Exception as e:
            logger.error(f"Error saving query: {e}")
            return None
    
    def get_saved_queries(self, limit: int = 50, offset: int = 0) -> List[SavedQuery]:
        """Get saved queries from the database."""
        try:
            import json
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, question, sql_query, tables_used, created_at, is_successful, error_message, query_results, result_message
                    FROM saved_queries
                    ORDER BY created_at DESC
                    OFFSET ? ROWS FETCH NEXT ? ROWS ONLY
                """, (offset, limit))
                
                queries = []
                for row in cursor.fetchall():
                    tables_used = row[3].split(',') if row[3] else []
                    
                    # Parse JSON results
                    query_results = None
                    if row[7]:
                        try:
                            query_results = json.loads(row[7])
                        except:
                            query_results = None
                    
                    queries.append(SavedQuery(
                        id=row[0],
                        question=row[1],
                        sql_query=row[2],
                        tables_used=tables_used,
                        created_at=row[4],
                        is_successful=bool(row[5]),
                        error_message=row[6],
                        query_results=query_results,
                        result_message=row[8]
                    ))
                
                logger.info(f"Retrieved {len(queries)} saved queries")
                return queries
                
        except Exception as e:
            logger.error(f"Error retrieving saved queries: {e}")
            return []
    
    def delete_saved_query(self, query_id: int) -> bool:
        """Delete a saved query by ID."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("DELETE FROM saved_queries WHERE id = ?", (query_id,))
                rows_affected = cursor.rowcount
                conn.commit()
                
                if rows_affected > 0:
                    logger.info(f"Deleted query with ID: {query_id}")
                    return True
                else:
                    logger.warning(f"Query with ID {query_id} not found")
                    return False
                    
        except Exception as e:
            logger.error(f"Error deleting query: {e}")
            return False
    
    def get_saved_query_by_id(self, query_id: int) -> Optional[SavedQuery]:
        """Get a specific saved query by ID."""
        try:
            import json
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, question, sql_query, tables_used, created_at, is_successful, error_message, query_results, result_message
                    FROM saved_queries
                    WHERE id = ?
                """, (query_id,))
                
                row = cursor.fetchone()
                if row:
                    tables_used = row[3].split(',') if row[3] else []
                    
                    # Parse JSON results
                    query_results = None
                    if row[7]:
                        try:
                            query_results = json.loads(row[7])
                        except:
                            query_results = None
                    
                    return SavedQuery(
                        id=row[0],
                        question=row[1],
                        sql_query=row[2],
                        tables_used=tables_used,
                        created_at=row[4],
                        is_successful=bool(row[5]),
                        error_message=row[6],
                        query_results=query_results,
                        result_message=row[8]
                    )
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving query by ID: {e}")
            return None
    
