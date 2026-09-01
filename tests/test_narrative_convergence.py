from app.analytics.narrative_convergence import narrative_convergence

def test_narrative_convergence():
    k1 = ['economy', 'inflation', 'trade']
    k2 = ['economy', 'inflation', 'markets']
    res = narrative_convergence.calculate_convergence(k1, k2)
    assert res['similarity_score'] > 0.4
    assert 'economy' in res['shared_topics']
