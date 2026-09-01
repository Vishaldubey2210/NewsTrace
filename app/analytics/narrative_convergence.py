class NarrativeConvergenceAnalyzer:
    """Measures how closely two or more outlets share framing words and coverage angles"""
    def calculate_convergence(self, k1, k2):
        s1, s2 = set(k1), set(k2)
        if not s1 or not s2: return {'similarity_score': 0.0}
        sim = round(len(s1 & s2) / len(s1 | s2), 3)
        return {'similarity_score': sim, 'shared_topics': list(s1 & s2)[:5]}

narrative_convergence = NarrativeConvergenceAnalyzer()
