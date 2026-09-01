class JournalistRanker:
    """Composite ranking algorithm weighing coverage volume and credibility"""
    def rank_journalists(self, journalists):
        for j in journalists:
            j['composite_score'] = round(j.get('article_count', 0) * 0.5 + j.get('credibility_score', 75) * 0.5, 1)
        journalists.sort(key=lambda x: x.get('composite_score', 0), reverse=True)
        return journalists

journalist_ranker = JournalistRanker()
