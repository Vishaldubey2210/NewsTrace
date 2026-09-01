class SensationalismScorer:
    """Scores sensationalism based on exclamation marks, superlatives, and ALL-CAPS words"""
    def score_headline(self, headline):
        if not headline: return {'score': 0.0, 'level': 'Low'}
        ex = headline.count('!')
        caps = sum(1 for w in headline.split() if len(w) > 2 and w.isupper())
        score = min(1.0, round((ex * 0.3) + (caps * 0.2), 2))
        level = 'High' if score > 0.6 else ('Moderate' if score > 0.3 else 'Low')
        return {'score': score, 'level': level}

sensationalism_scorer = SensationalismScorer()
