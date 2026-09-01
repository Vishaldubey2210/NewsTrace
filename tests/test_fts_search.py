from app.database.fts_search import fts_search_engine

def test_fts_search():
    res = fts_search_engine.search("Technology")
    assert isinstance(res, list)
