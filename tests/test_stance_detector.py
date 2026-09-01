from app.nlp.stance_detector import stance_detector

def test_stance_detection():
    text = "Officials praised the prime minister for successful economic reforms."
    res = stance_detector.detect_stance(text, "prime minister")
    assert res['stance'] == 'Favor'
