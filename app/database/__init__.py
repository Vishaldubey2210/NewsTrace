"""
NewsTrace Database Module
Database operations initialization
"""

from app.database.sqlite_db import db_manager, init_db

__all__ = [
    'db_manager',
    'init_db'
]
