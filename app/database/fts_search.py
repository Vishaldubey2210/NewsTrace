import sqlite3

class FTSSearchEngine:
    """Full-text search engine"""
    def search(self, query):
        return [{'title': f'Match for {query}'}]

fts_search_engine = FTSSearchEngine()
