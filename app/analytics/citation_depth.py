class CitationDepthAnalyzer:
    """Evaluates journalistic rigor based on primary source attributions"""
    def evaluate_depth(self, text):
        count = text.lower().count('according to') + text.lower().count('study shows')
        return {'depth_score': min(100, count * 20), 'tier': 'High' if count >= 3 else 'Standard'}

citation_depth_analyzer = CitationDepthAnalyzer()
