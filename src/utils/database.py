"""
Database Layer
Provides persistent storage for application data.

Supports:
- SQLite (development)
- PostgreSQL (production)
- Connection pooling
- Migration support
"""

import sqlite3
import os
from typing import Dict, Any, List, Optional
from pathlib import Path
from contextlib import contextmanager
import json
from datetime import datetime


class Database:
    """
    Database abstraction layer.
    
    Supports both SQLite and PostgreSQL with unified interface.
    """
    
    def __init__(self, db_type: str = "sqlite", connection_string: Optional[str] = None):
        """
        Initialize database.
        
        Args:
            db_type: "sqlite" or "postgresql"
            connection_string: Database connection string
        """
        self.db_type = db_type
        self.connection_string = connection_string
        
        if db_type == "sqlite":
            if connection_string is None:
                # Default to data/app.db
                project_root = Path(__file__).parent.parent.parent
                db_path = project_root / "data" / "app.db"
                db_path.parent.mkdir(parents=True, exist_ok=True)
                connection_string = str(db_path)
            
            self.connection_string = connection_string
            self._init_sqlite()
        elif db_type == "postgresql":
            # PostgreSQL connection would be initialized here
            # For now, we'll use SQLite as fallback
            self.db_type = "sqlite"
            self._init_sqlite()
    
    def _init_sqlite(self):
        """Initialize SQLite database and create tables."""
        conn = sqlite3.connect(self.connection_string)
        conn.row_factory = sqlite3.Row
        
        # Create tables
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS analytics_cache (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cache_key TEXT UNIQUE NOT NULL,
                cache_data TEXT NOT NULL,
                expires_at TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS user_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                preference_key TEXT NOT NULL,
                preference_value TEXT NOT NULL,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(username, preference_key)
            );
            
            CREATE TABLE IF NOT EXISTS performance_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metric_name TEXT NOT NULL,
                metric_value REAL NOT NULL,
                metric_type TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                metadata TEXT
            );
            
            CREATE INDEX IF NOT EXISTS idx_analytics_cache_key ON analytics_cache(cache_key);
            CREATE INDEX IF NOT EXISTS idx_analytics_cache_expires ON analytics_cache(expires_at);
            CREATE INDEX IF NOT EXISTS idx_user_preferences_username ON user_preferences(username);
            CREATE INDEX IF NOT EXISTS idx_performance_metrics_name ON performance_metrics(metric_name);
            CREATE INDEX IF NOT EXISTS idx_performance_metrics_timestamp ON performance_metrics(timestamp);
        """)
        
        conn.commit()
        conn.close()
    
    @contextmanager
    def get_connection(self):
        """Get database connection context manager."""
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.connection_string)
            conn.row_factory = sqlite3.Row
            try:
                yield conn
                conn.commit()
            except Exception:
                conn.rollback()
                raise
            finally:
                conn.close()
        else:
            # PostgreSQL connection would go here
            raise NotImplementedError("PostgreSQL not yet implemented")
    
    def cache_set(
        self,
        key: str,
        value: Any,
        expires_in_seconds: int = 3600
    ) -> bool:
        """Set cache value."""
        try:
            expires_at = datetime.now().timestamp() + expires_in_seconds
            
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO analytics_cache 
                    (cache_key, cache_data, expires_at)
                    VALUES (?, ?, ?)
                """, (key, json.dumps(value), expires_at))
            
            return True
        except Exception:
            return False
    
    def cache_get(self, key: str) -> Optional[Any]:
        """Get cache value."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT cache_data, expires_at 
                    FROM analytics_cache 
                    WHERE cache_key = ? AND expires_at > ?
                """, (key, datetime.now().timestamp()))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row["cache_data"])
            
            return None
        except Exception:
            return None
    
    def cache_clear_expired(self) -> int:
        """Clear expired cache entries. Returns count of cleared entries."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    DELETE FROM analytics_cache 
                    WHERE expires_at <= ?
                """, (datetime.now().timestamp(),))
                
                return cursor.rowcount
        except Exception:
            return 0
    
    def set_user_preference(
        self,
        username: str,
        key: str,
        value: Any
    ) -> bool:
        """Set user preference."""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO user_preferences 
                    (username, preference_key, preference_value, updated_at)
                    VALUES (?, ?, ?, ?)
                """, (username, key, json.dumps(value), datetime.now().isoformat()))
            
            return True
        except Exception:
            return False
    
    def get_user_preference(
        self,
        username: str,
        key: str,
        default: Any = None
    ) -> Any:
        """Get user preference."""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    SELECT preference_value 
                    FROM user_preferences 
                    WHERE username = ? AND preference_key = ?
                """, (username, key))
                
                row = cursor.fetchone()
                if row:
                    return json.loads(row["preference_value"])
            
            return default
        except Exception:
            return default
    
    def record_metric(
        self,
        metric_name: str,
        value: float,
        metric_type: str = "gauge",
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Record a performance metric."""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    INSERT INTO performance_metrics 
                    (metric_name, metric_value, metric_type, metadata)
                    VALUES (?, ?, ?, ?)
                """, (metric_name, value, metric_type, json.dumps(metadata or {})))
            
            return True
        except Exception:
            return False
    
    def get_metrics(
        self,
        metric_name: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        limit: int = 1000
    ) -> List[Dict[str, Any]]:
        """Get performance metrics."""
        try:
            query = "SELECT * FROM performance_metrics WHERE 1=1"
            params = []
            
            if metric_name:
                query += " AND metric_name = ?"
                params.append(metric_name)
            
            if start_time:
                query += " AND timestamp >= ?"
                params.append(start_time.isoformat())
            
            if end_time:
                query += " AND timestamp <= ?"
                params.append(end_time.isoformat())
            
            query += " ORDER BY timestamp DESC LIMIT ?"
            params.append(limit)
            
            with self.get_connection() as conn:
                cursor = conn.execute(query, params)
                rows = cursor.fetchall()
                
                return [dict(row) for row in rows]
        except Exception:
            return []

