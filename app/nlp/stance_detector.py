class StanceDetector:
    """Detects subjective author stance (Favor, Against, Neutral) towards identified named entities"""
    def detect_stance(self, text, entity_name):
        if not text or not entity_name:
            return {'stance': 'Neutral', 'confidence': 0.5}
        lower_text = text.lower()
        lower_entity = entity_name.lower()
        if lower_entity not in lower_text:
            return {'stance': 'Neutral', 'confidence': 0.0}
        sentences = [s for s in lower_text.split('.') if lower_entity in s]
        pos = sum(1 for s in sentences for w in {'praised', 'achieved', 'supported'} if w in s)
        neg = sum(1 for s in sentences for w in {'criticized', 'failed', 'opposed'} if w in s)
        if pos > neg:
            return {'stance': 'Favor', 'confidence': 0.8}
        elif neg > pos:
            return {'stance': 'Against', 'confidence': 0.8}
        return {'stance': 'Neutral', 'confidence': 0.6}

stance_detector = StanceDetector()
