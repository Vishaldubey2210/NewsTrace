from app.analytics.citation_depth import citation_depth_analyzer

def test_citation_depth():
    text = "According to official reports, the study shows promising trends."
    res = citation_depth_analyzer.evaluate_depth(text)
    assert res['depth_score'] > 0
