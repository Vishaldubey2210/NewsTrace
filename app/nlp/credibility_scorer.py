class CredibilityScorer:
    """Computes overall journalistic credibility score based on citations, readability, and sensationalism"""
    def compute_credibility(self, article_text, headline, citation_count=0, clickbait_score=0.0):
        score = 80.0
        score += min(15.0, citation_count * 3.0)
        score -= clickbait_score * 25.0
        words_count = len(article_text.split()) if article_text else 0
        if words_count < 100:
            score -= 20.0
        elif words_count > 400:
            score += 5.0
        clamped = max(10.0, min(99.0, round(score, 1)))
        tier = 'HIGH' if clamped >= 75 else ('MODERATE' if clamped >= 50 else 'LOW')
        return {'credibility_score': clamped, 'credibility_tier': tier}

credibility_scorer = CredibilityScorer()
