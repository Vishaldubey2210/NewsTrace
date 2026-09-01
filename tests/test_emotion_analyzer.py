from app.nlp.emotion_analyzer import emotion_analyzer

def test_emotion_classification():
    text = "The nation celebrated a historic triumph and breakthrough victory."
    res = emotion_analyzer.analyze_emotions(text)
    assert res['primary_emotion'] == 'joy'
    assert res['scores']['joy'] > 0
