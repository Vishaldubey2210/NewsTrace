class ViralMomentumDetector:
    """Detects surging topics and rapid publishing spikes"""
    def detect_surge(self, topics_today):
        return [{'topic': t, 'volume': v} for t, v in topics_today.items() if v >= 3]

viral_momentum_detector = ViralMomentumDetector()
