from app.analytics.viral_momentum import viral_momentum_detector

def test_viral_momentum():
    surges = viral_momentum_detector.detect_surge({'AI': 5, 'Sports': 1})
    assert len(surges) >= 1
    assert surges[0]['topic'] == 'AI'
