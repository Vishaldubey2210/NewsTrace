"""Unit tests for SQLite database operations."""
from app.database.sqlite_db import DatabaseManager

def test_database_initialization(tmp_path):
    db_file = tmp_path / "test_news.db"
    db = DatabaseManager(str(db_file))
    assert db is not None
