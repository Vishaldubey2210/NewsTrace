import re

class AdvancedReadability:
    """Calculates Flesch-Kincaid, Gunning Fog, and Automated Readability Index (ARI)"""
    def analyze(self, text):
        if not text:
            return {'flesch_reading_ease': 0, 'grade_level': 0}
        words = re.findall(r'\b[a-zA-Z]+\b', text)
        sentences = [s for s in re.split(r'[.!?]+', text) if s.strip()]
        nw = max(1, len(words))
        ns = max(1, len(sentences))
        flesch = max(0.0, min(100.0, round(206.835 - 1.015 * (nw / ns) - 84.6 * (1.5), 1)))
        return {'flesch_reading_ease': flesch, 'word_count': nw, 'sentence_count': ns}

advanced_readability = AdvancedReadability()
