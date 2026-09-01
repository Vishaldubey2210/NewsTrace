import re

class EmotionAnalyzer:
    """Classifies primary emotional tone (joy, anger, fear, sadness, surprise, neutral) in news articles"""
    def __init__(self):
        self.emotion_lexicons = {
            'joy': {'triumph', 'celebration', 'progress', 'delight', 'optimism', 'victory', 'thriving', 'praise'},
            'anger': {'outrage', 'fury', 'condemn', 'betrayal', 'slammed', 'blasted', 'hostile', 'unjust'},
            'fear': {'threat', 'collapse', 'warning', 'panic', 'escalation', 'danger', 'catastrophe', 'dread'},
            'sadness': {'tragedy', 'mourn', 'grief', 'casualty', 'loss', 'devastating', 'sorrow', 'bereaved'},
            'surprise': {'unexpected', 'shocking', 'astonishing', 'unprecedented', 'dramatic', 'stunning'}
        }

    def analyze_emotions(self, text):
        if not text:
            return {'primary_emotion': 'neutral', 'scores': {}}
        words = re.findall(r'\b\w+\b', text.lower())
        total_words = max(1, len(words))
        scores = {}
        for emotion, lexicon in self.emotion_lexicons.items():
            matches = sum(1 for w in words if w in lexicon)
            scores[emotion] = round(matches / total_words * 100, 2)
        primary = max(scores, key=scores.get)
        if scores[primary] == 0:
            primary = 'neutral'
        return {'primary_emotion': primary, 'scores': scores}

emotion_analyzer = EmotionAnalyzer()
