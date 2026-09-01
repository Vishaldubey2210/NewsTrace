import re

class QuoteExtractor:
    """Extracts direct quotes and attributed statements with speaker context"""
    def extract_quotes(self, text):
        if not text: return []
        quotes = re.findall(r'["“]([^"”]{10,200})["”]', text)
        return [{'quote': q.strip()} for q in quotes[:10]]

quote_extractor = QuoteExtractor()
