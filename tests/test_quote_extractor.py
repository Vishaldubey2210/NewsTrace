from app.nlp.quote_extractor import quote_extractor

def test_quote_extraction():
    text = '“We will achieve the target ahead of schedule,” said Minister Kumar.'
    quotes = quote_extractor.extract_quotes(text)
    assert len(quotes) >= 1
