class TopicDriftTracker:
    """Tracks how a journalist's core beats evolve"""
    def compute_drift(self, past, recent):
        return {'new_beats': list(set(recent) - set(past))}

topic_drift_tracker = TopicDriftTracker()
