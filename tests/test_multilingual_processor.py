from app.nlp.multilingual_processor import multilingual_processor

def test_language_detection():
    assert multilingual_processor.detect_language("English text headline") == 'en'
    assert multilingual_processor.detect_language("यह हिंदी समाचार है।") == 'hi'
