"""
Configuration management for SQL Agent application.
Handles environment variables and application settings.
"""
import os
import sys
from dotenv import load_dotenv
from typing import Optional

# Load environment variables
# PyInstaller için .env dosyasını bundle içinden yükle
if getattr(sys, 'frozen', False):
    # PyInstaller bundle içindeyiz
    import sys
    bundle_dir = sys._MEIPASS
    env_path = os.path.join(bundle_dir, '.env')
    if os.path.exists(env_path):
        load_dotenv(env_path)
    else:
        # .env bulunamazsa, executable'ın yanında ara
        exe_dir = os.path.dirname(sys.executable)
        env_path = os.path.join(exe_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
else:
    load_dotenv()


class Config:
    """Application configuration class."""
    
    # Flask Configuration
    SECRET_KEY: str = os.getenv('SECRET_KEY', os.urandom(24))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # OpenAI Configuration
    OPENAI_API_KEY: Optional[str] = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL: str = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
    
    # Database Configuration
    DB_CONNECTION_TIMEOUT: int = int(os.getenv('DB_CONNECTION_TIMEOUT', '5'))
    DEFAULT_ODBC_DRIVER: str = os.getenv('DEFAULT_ODBC_DRIVER', 'ODBC Driver 17 for SQL Server')
    KEYRING_SERVICE: str = os.getenv('KEYRING_SERVICE', 'sql-agent-cursor')
    
    # Application Configuration
    MAX_TABLES_PER_QUERY: int = int(os.getenv('MAX_TABLES_PER_QUERY', '10'))
    MAX_QUERY_LENGTH: int = int(os.getenv('MAX_QUERY_LENGTH', '1000'))
    
    @classmethod
    def validate_config(cls) -> None:
        """Validate required configuration values."""
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY environment variable is required")
    
    @classmethod
    def get_openai_config(cls) -> dict:
        """Get OpenAI configuration as dictionary."""
        return {
            'api_key': cls.OPENAI_API_KEY
        }
