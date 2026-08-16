"""Unit tests for NLP sentiment analyzer and entity extraction."""
from app.nlp.sentiment_analyzer import SentimentAnalyzer
from app.nlp.entity_extractor import EntityExtractor

def test_sentiment_analyzer_positive():
    analyzer = SentimentAnalyzer()
    res = analyzer.analyze("The economy showed magnificent growth and incredible breakthrough results.")
    assert "polarity" in res
    assert res["polarity"] > 0

def test_sentiment_analyzer_negative():
    analyzer = SentimentAnalyzer()
    res = analyzer.analyze("The disaster caused devastating failure and terrible destruction.")
    assert res["polarity"] < 0

def test_entity_extractor():
    extractor = EntityExtractor()
    entities = extractor.extract_entities("Apple Inc. announced the new iPhone in California.")
    assert isinstance(entities, list)
