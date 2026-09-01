import math

class OutletDiversityIndex:
    """Calculates topical coverage diversity index"""
    def calculate_entropy(self, topic_counts):
        total = sum(topic_counts.values())
        if total == 0: return 0.0
        return round(-sum((c/total) * math.log2(c/total) for c in topic_counts.values() if c > 0), 2)

outlet_diversity_index = OutletDiversityIndex()
