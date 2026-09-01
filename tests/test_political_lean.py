from app.analytics.political_lean_analyzer import political_lean_analyzer

def test_political_lean_evaluation():
    articles = ["Strong focus on progressive welfare and labor rights inequality reduction."]
    res = political_lean_analyzer.evaluate_lean(articles)
    assert res['lean'] in ['Left', 'Center-Left']
