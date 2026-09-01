class FramingDiffAnalyzer:
    """Analyzes differences in keyword emphasis between left vs right reporting"""
    def compare_framing(self, k1, k2):
        s1, s2 = set(k1), set(k2)
        return {'outlet_1_emphasis': list(s1 - s2)[:5], 'outlet_2_emphasis': list(s2 - s1)[:5]}

framing_diff_analyzer = FramingDiffAnalyzer()
