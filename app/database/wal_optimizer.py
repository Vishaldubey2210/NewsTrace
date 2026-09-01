import sqlite3

class WALOptimizer:
    """Configures SQLite WAL mode"""
    @staticmethod
    def apply(db_path):
        try:
            conn = sqlite3.connect(db_path)
            conn.execute("PRAGMA journal_mode=WAL;")
            conn.close()
        except Exception:
            pass

wal_optimizer = WALOptimizer()
