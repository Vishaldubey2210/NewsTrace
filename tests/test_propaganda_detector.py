from app.nlp.propaganda_detector import propaganda_detector

def test_propaganda_flagging():
    text = "This is a tyrannical and monstrous plot threatening imminent doom!"
    res = propaganda_detector.detect_techniques(text)
    assert res['flagged'] is True
    assert res['total_flags'] >= 2
