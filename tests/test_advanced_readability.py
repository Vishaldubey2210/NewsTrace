from app.nlp.advanced_readability import advanced_readability

def test_readability_indices():
    text = "The quick brown fox jumps over the lazy dog. Simple sentences are easy to read."
    res = advanced_readability.analyze(text)
    assert res['flesch_reading_ease'] > 0
    assert res['word_count'] > 5
