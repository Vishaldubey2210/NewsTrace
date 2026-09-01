from app.nlp.credibility_scorer import credibility_scorer

def test_credibility_calculation():
    res = credibility_scorer.compute_credibility("Detailed 500 words article with citations.", "Normal Title", citation_count=3, clickbait_score=0.1)
    assert res['credibility_score'] >= 75
    assert res['credibility_tier'] == 'HIGH'
