class MultilingualProcessor:
    """Detects article language and normalizes cross-lingual journalistic entities"""
    def detect_language(self, text):
        if not text: return 'en'
        if any('\u0900' <= c <= '\u097F' for c in text): return 'hi'
        return 'en'

multilingual_processor = MultilingualProcessor()
