from app.nlp.sensationalism_scorer import sensationalism_scorer

def test_sensationalism_scoring():
    res = sensationalism_scorer.score_headline("SHOCKING DISASTER! The Greatest Historic Crisis Ever!")
    assert res['score'] > 0.5
    assert res['level'] == 'High'
