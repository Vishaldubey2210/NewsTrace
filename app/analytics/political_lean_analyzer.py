class PoliticalLeanAnalyzer:
    """Estimates political spectrum leaning based on rhetoric vocabulary and framing markers"""
    def __init__(self):
        self.left_markers = {'progressive', 'welfare', 'inequality', 'climate justice', 'labor'}
        self.right_markers = {'deregulation', 'free market', 'fiscal discipline', 'tradition', 'border'}

    def evaluate_lean(self, articles_text_list):
        if not articles_text_list:
            return {'lean': 'Center', 'score': 0.0}
        combined = " ".join(articles_text_list).lower()
        l_hits = sum(1 for m in self.left_markers if m in combined)
        r_hits = sum(1 for m in self.right_markers if m in combined)
        total = l_hits + r_hits
        if total == 0:
            return {'lean': 'Center', 'score': 0.0}
        ratio = (r_hits - l_hits) / total
        lean = 'Center'
        if ratio <= -0.3: lean = 'Left'
        elif ratio < -0.1: lean = 'Center-Left'
        elif ratio >= 0.3: lean = 'Right'
        elif ratio > 0.1: lean = 'Center-Right'
        return {'lean': lean, 'score': round(ratio, 2)}

political_lean_analyzer = PoliticalLeanAnalyzer()
