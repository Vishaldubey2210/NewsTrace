"""
Database Query Helpers
Pre-compiled SQL queries and execution wrappers for article retrieval, filtering, and aggregation.
"""

from app.database.sqlite_db import DatabaseManager

class QueryManager:
    """Executes optimized database queries for articles and analytics."""

    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_articles_by_outlet(self, outlet: str, limit: int = 50):
        query = "SELECT * FROM articles WHERE source = ? ORDER BY published_date DESC LIMIT ?"
        return self.db.fetch_all(query, (outlet, limit))

    def get_sentiment_trends(self, limit: int = 30):
        query = """
            SELECT source, AVG(sentiment_score) as avg_sentiment, COUNT(*) as article_count
            FROM articles
            WHERE sentiment_score IS NOT NULL
            GROUP BY source
            ORDER BY article_count DESC
            LIMIT ?
        """
        return self.db.fetch_all(query, (limit,))

    def get_top_entities(self, limit: int = 20):
        query = """
            SELECT entity_name, entity_type, COUNT(*) as frequency
            FROM entities
            GROUP BY entity_name, entity_type
            ORDER BY frequency DESC
            LIMIT ?
        """
        return self.db.fetch_all(query, (limit,))
