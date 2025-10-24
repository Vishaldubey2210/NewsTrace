"""
NewsTrace Influence Score
Calculate journalist influence using custom algorithm
"""

import logging
from typing import List, Dict
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class InfluenceScoreCalculator:
    """Calculate journalist influence scores"""
    
    def __init__(self):
        # Weights for different factors
        self.weights = {
            'article_count': 0.4,
            'topic_diversity': 0.3,
            'recency': 0.2,
            'profile_completeness': 0.1
        }
    
    def calculate_influence(self, journalist: Dict) -> float:
        """
        Calculate influence score (0-100)
        
        Factors:
        - Article count (more = better)
        - Topic diversity (broader coverage = better)
        - Recency (recent activity = better)
        - Profile completeness (more info = better)
        """
        
        scores = {}
        
        # 1. Article Count Score (0-100)
        article_count = journalist.get('article_count', 0)
        scores['article_count'] = min(article_count * 2, 100)
        
        # 2. Topic Diversity Score (0-100)
        # More topics = higher score
        topics = journalist.get('topics', [])
        scores['topic_diversity'] = min(len(topics) * 20, 100)
        
        # 3. Recency Score (0-100)
        last_updated = journalist.get('last_updated')
        if last_updated:
            try:
                if isinstance(last_updated, str):
                    last_updated = datetime.fromisoformat(last_updated)
                
                days_ago = (datetime.now() - last_updated).days
                scores['recency'] = max(100 - (days_ago * 2), 0)
            except:
                scores['recency'] = 50
        else:
            scores['recency'] = 50
        
        # 4. Profile Completeness Score (0-100)
        fields = ['bio', 'contact_email', 'profile_url', 'beat', 'twitter_handle']
        filled = sum(1 for f in fields if journalist.get(f))
        scores['profile_completeness'] = (filled / len(fields)) * 100
        
        # Calculate weighted score
        total_score = sum(
            scores[factor] * weight 
            for factor, weight in self.weights.items()
        )
        
        return round(total_score, 2)
    
    def rank_journalists(self, journalists: List[Dict]) -> List[Dict]:
        """Rank journalists by influence score"""
        
        # Calculate scores
        for journalist in journalists:
            journalist['influence_score'] = self.calculate_influence(journalist)
        
        # Sort by score (descending)
        ranked = sorted(journalists, key=lambda x: x.get('influence_score', 0), reverse=True)
        
        return ranked


# Global instance
influence_calculator = InfluenceScoreCalculator()
