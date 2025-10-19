"""
Data models for SQL Agent application.
Defines data structures and validation.
"""
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from enum import Enum
from datetime import datetime


class QueryType(Enum):
    """Types of SQL queries."""
    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    OTHER = "OTHER"


@dataclass
class DatabaseConnection:
    """Database connection information."""
    connection_string: str
    timeout: int = 5
    
    def __post_init__(self):
        """Validate connection string."""
        if not self.connection_string:
            raise ValueError("Connection string cannot be empty")


@dataclass
class TableInfo:
    """Information about a database table."""
    name: str
    columns: List[str]
    
    def __post_init__(self):
        """Validate table information."""
        if not self.name:
            raise ValueError("Table name cannot be empty")
        if not self.columns:
            raise ValueError("Table must have at least one column")


@dataclass
class QueryRequest:
    """Request for natural language to SQL conversion."""
    question: str
    tables: List[str]
    
    def __post_init__(self):
        """Validate query request."""
        if not self.question.strip():
            raise ValueError("Question cannot be empty")
        if not self.tables:
            raise ValueError("At least one table must be specified")
        if len(self.tables) > 10:  # Configurable limit
            raise ValueError("Too many tables specified")


@dataclass
class QueryResponse:
    """Response from SQL query execution."""
    sql_query: str
    query_type: QueryType
    results: Optional[List[Dict[str, Any]]] = None
    message: Optional[str] = None
    error: Optional[str] = None
    row_count: Optional[int] = None
    
    @property
    def is_successful(self) -> bool:
        """Check if query was successful."""
        return self.error is None
    
    @property
    def is_select_query(self) -> bool:
        """Check if this is a SELECT query."""
        return self.query_type == QueryType.SELECT


@dataclass
class DatabaseSchema:
    """Complete database schema information."""
    tables: Dict[str, TableInfo]
    
    def get_table_names(self) -> List[str]:
        """Get list of table names."""
        return list(self.tables.keys())
    
    def get_table_columns(self, table_name: str) -> List[str]:
        """Get columns for a specific table."""
        if table_name not in self.tables:
            raise ValueError(f"Table '{table_name}' not found in schema")
        return self.tables[table_name].columns


@dataclass
class SavedQuery:
    """Saved query information."""
    id: Optional[int] = None
    question: str = ""
    sql_query: str = ""
    tables_used: List[str] = None
    created_at: Optional[datetime] = None
    is_successful: bool = True
    error_message: Optional[str] = None
    query_results: Optional[List[Dict[str, Any]]] = None
    result_message: Optional[str] = None
    is_scheduled: bool = False
    
    def __post_init__(self):
        """Initialize default values."""
        if self.tables_used is None:
            self.tables_used = []
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'question': self.question,
            'sql_query': self.sql_query,
            'tables_used': self.tables_used,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_successful': self.is_successful,
            'error_message': self.error_message,
            'query_results': self.query_results,
            'result_message': self.result_message,
            'is_scheduled': self.is_scheduled
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SavedQuery':
        """Create from dictionary."""
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        
        return cls(
            id=data.get('id'),
            question=data.get('question', ''),
            sql_query=data.get('sql_query', ''),
            tables_used=data.get('tables_used', []),
            created_at=created_at,
            is_successful=data.get('is_successful', True),
            error_message=data.get('error_message'),
            query_results=data.get('query_results'),
            result_message=data.get('result_message'),
            is_scheduled=data.get('is_scheduled', False)
        )


@dataclass
class ScheduledQuery:
    """Scheduled query information."""
    id: Optional[int] = None
    question: str = ""
    tables_used: List[str] = None
    schedule_type: str = "daily"  # hourly, daily, weekly, monthly, custom
    schedule_time: Optional[str] = None  # HH:MM format
    schedule_day: Optional[int] = None  # For weekly (0-6) or monthly (1-31)
    cron_expression: Optional[str] = None  # For custom schedules
    is_active: bool = True
    created_at: Optional[datetime] = None
    last_run_at: Optional[datetime] = None
    last_run_status: Optional[str] = None
    run_count: int = 0
    
    def __post_init__(self):
        """Initialize default values."""
        if self.tables_used is None:
            self.tables_used = []
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'question': self.question,
            'tables_used': self.tables_used,
            'schedule_type': self.schedule_type,
            'schedule_time': self.schedule_time,
            'schedule_day': self.schedule_day,
            'cron_expression': self.cron_expression,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'last_run_status': self.last_run_status,
            'run_count': self.run_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ScheduledQuery':
        """Create from dictionary."""
        created_at = None
        if data.get('created_at'):
            created_at = datetime.fromisoformat(data['created_at'].replace('Z', '+00:00'))
        
        last_run_at = None
        if data.get('last_run_at'):
            last_run_at = datetime.fromisoformat(data['last_run_at'].replace('Z', '+00:00'))
        
        return cls(
            id=data.get('id'),
            question=data.get('question', ''),
            tables_used=data.get('tables_used', []),
            schedule_type=data.get('schedule_type', 'daily'),
            schedule_time=data.get('schedule_time'),
            schedule_day=data.get('schedule_day'),
            cron_expression=data.get('cron_expression'),
            is_active=data.get('is_active', True),
            created_at=created_at,
            last_run_at=last_run_at,
            last_run_status=data.get('last_run_status'),
            run_count=data.get('run_count', 0)
        )
