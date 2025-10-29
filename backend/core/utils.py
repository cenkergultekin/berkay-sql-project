"""
Utility functions for SQL Agent application.
Common helper functions and validators.
"""
import re
from typing import List, Dict, Any, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class SQLValidator:
    """Utility class for SQL validation and sanitization."""
    
    # Potentially dangerous SQL keywords
    DANGEROUS_KEYWORDS = [
        'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'EXEC', 'EXECUTE',
        'SP_', 'XP_', 'SHUTDOWN', 'BACKUP', 'RESTORE'
    ]
    
    @classmethod
    def validate_sql_query(cls, sql_query: str) -> bool:
        """
        Validate SQL query for security and basic syntax.
        
        Args:
            sql_query: SQL query string to validate
            
        Returns:
            True if query is valid, False otherwise
        """
        if not sql_query or not sql_query.strip():
            return False
        
        sql_upper = sql_query.upper().strip()
        
        # Check for dangerous keywords
        for keyword in cls.DANGEROUS_KEYWORDS:
            if keyword in sql_upper:
                logger.warning(f"Dangerous keyword detected: {keyword}")
                return False
        
        # Basic syntax validation
        if not cls._has_valid_sql_structure(sql_upper):
            return False
        
        return True
    
    @classmethod
    def _has_valid_sql_structure(cls, sql_upper: str) -> bool:
        """Check if SQL has valid basic structure."""
        # Must start with a valid SQL keyword
        valid_starters = ['SELECT', 'INSERT', 'UPDATE', 'DELETE', 'WITH']
        if not any(sql_upper.startswith(starter) for starter in valid_starters):
            return False
        
        # Basic bracket matching
        if sql_upper.count('(') != sql_upper.count(')'):
            return False
        
        return True


class StringUtils:
    """Utility functions for string operations."""
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 1000) -> str:
        """
        Sanitize user input by removing dangerous characters and limiting length.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
            logger.warning(f"Input truncated to {max_length} characters")
        
        return sanitized.strip()
    
    @staticmethod
    def format_table_list(tables: List[str]) -> str:
        """Format list of tables for display."""
        if not tables:
            return "No tables selected"
        
        if len(tables) == 1:
            return f"Table: {tables[0]}"
        
        return f"Tables: {', '.join(tables)}"


class ResponseFormatter:
    """Utility class for formatting API responses."""
    
    @staticmethod
    def format_error_response(error_message: str, error_code: str = "GENERIC_ERROR") -> Dict[str, Any]:
        """Format error response for API."""
        return {
            "success": False,
            "error": error_message,
            "error_code": error_code
        }
    
    @staticmethod
    def format_success_response(data: Any, message: Optional[str] = None) -> Dict[str, Any]:
        """Format success response for API."""
        response = {
            "success": True,
            "data": data
        }
        
        if message:
            response["message"] = message
        
        return response
    
    @staticmethod
    def format_query_response(query_response) -> Dict[str, Any]:
        """Format query response for API."""
        if query_response.is_successful:
            if query_response.is_select_query:
                return {
                    "success": True,
                    "sql": query_response.sql_query,
                    "results": query_response.results,
                    "row_count": len(query_response.results) if query_response.results else 0
                }
            else:
                return {
                    "success": True,
                    "sql": query_response.sql_query,
                    "message": query_response.message,
                    "row_count": query_response.row_count
                }
        else:
            return {
                "success": False,
                "error": query_response.error,
                "sql": query_response.sql_query
            }


class LoggingUtils:
    """Utility functions for logging."""
    
    @staticmethod
    def setup_logging(level: str = "INFO") -> None:
        """Setup application logging."""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
    
    @staticmethod
    def log_request_info(endpoint: str, user_data: Dict[str, Any]) -> None:
        """Log request information for debugging."""
        logger.info(f"Request to {endpoint}: {user_data}")
    
    @staticmethod
    def log_response_info(endpoint: str, success: bool, response_data: Any) -> None:
        """Log response information for debugging."""
        status = "SUCCESS" if success else "ERROR"
        logger.info(f"Response from {endpoint} - {status}: {response_data}")


class ODBCUtils:
    """Helpers for ODBC connection string handling and masking."""

    SENSITIVE_KEYS = {"PWD", "PASSWORD"}

    @staticmethod
    def parse_dsn(dsn: str) -> Dict[str, str]:
        """Parse a semicolon-separated ODBC connection string into a dict.

        Example: "DRIVER={ODBC Driver 17 for SQL Server};SERVER=127.0.0.1;DATABASE=test;UID=sa;PWD=secret"
        """
        if not dsn:
            return {}
        parts = [p.strip() for p in dsn.split(";") if p.strip()]
        result: Dict[str, str] = {}
        for part in parts:
            if "=" not in part:
                continue
            key, value = part.split("=", 1)
            key = key.strip().upper()
            value = value.strip()
            # Normalize common keys
            if key == "USER" or key == "USERNAME":
                key = "UID"
            if key == "PWD" or key == "PASSWORD":
                key = "PWD"
            if key == "SERVERNAME":
                key = "SERVER"
            if key == "DB" or key == "DATABASE_NAME":
                key = "DATABASE"
            result[key] = value
        return result

    @staticmethod
    def build_dsn(driver: str, server: str, database: str, uid: str, pwd: Optional[str] = None, extra: Optional[Dict[str, str]] = None) -> str:
        """Build an ODBC connection string. If pwd is None, omit it (for masked/logging)."""
        items: List[Tuple[str, str]] = []
        if driver:
            items.append(("DRIVER", f"{{{driver}}}" if not driver.startswith("{") else driver))
        if server:
            items.append(("SERVER", server))
        if database:
            items.append(("DATABASE", database))
        if uid:
            items.append(("UID", uid))
        if pwd is not None:
            items.append(("PWD", pwd))
        if extra:
            for k, v in extra.items():
                if k and v and k.upper() not in {k for k, _ in items}:
                    items.append((k, v))
        return ";".join(f"{k}={v}" for k, v in items)

    @staticmethod
    def mask_dsn(dsn: str) -> str:
        """Return a masked version of the DSN, hiding password values."""
        if not dsn:
            return dsn
        parts = [p.strip() for p in dsn.split(";") if p.strip()]
        masked: List[str] = []
        for part in parts:
            if "=" not in part:
                masked.append(part)
                continue
            key, value = part.split("=", 1)
            key_upper = key.strip().upper()
            if key_upper in ODBCUtils.SENSITIVE_KEYS:
                masked.append(f"{key}=***")
            else:
                masked.append(part)
        return ";".join(masked)

    @staticmethod
    def mask_dict(data: Dict[str, Any]) -> Dict[str, Any]:
        """Mask sensitive keys in a dict for safe logging."""
        if not data:
            return {}
        masked = {}
        for k, v in data.items():
            if isinstance(k, str) and k.upper() in ODBCUtils.SENSITIVE_KEYS:
                masked[k] = "***"
            elif isinstance(k, str) and k.lower() in {"password", "pwd"}:
                masked[k] = "***"
            else:
                masked[k] = v
        return masked
