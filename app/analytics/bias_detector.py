"""
NewsTrace Bias Detector
Detect potential bias in journalist coverage using statistical analysis
"""

import logging
from typing import List, Dict, Optional
from collections import Counter

logger = logging.getLogger(__name__)


class BiasDetector:
    """Detect potential bias in journalist coverage"""
    
    def __init__(self):
        # Bias indicator keywords
        self.political_left_keywords = [
            'progressive', 'liberal', 'equality', 'social justice', 'reform',
            'welfare', 'regulation', 'environment'
        ]
        
        self.political_right_keywords = [
            'conservative', 'traditional', 'free market', 'deregulation',
            'national security', 'patriotic', 'business'
        ]
        
        self.neutral_indicators = [
            'according to', 'reported', 'stated', 'official', 'data shows'
        ]
    
    def analyze_bias(self, text: str) -> Dict[str, float]:
        """
        Analyze text for potential political bias
        
        Args:
            text: Text content to analyze
            
        Returns:
            {
                'left_score': float,
                'right_score': float,
                'neutral_score': float,
                'bias_category': str,
                'confidence': float
            }
        """
        if not text:
            return self._neutral_bias()
        
        text_lower = text.lower()
        
        # Count keyword occurrences
        left_count = sum(1 for keyword in self.political_left_keywords if keyword in text_lower)
        right_count = sum(1 for keyword in self.political_right_keywords if keyword in text_lower)
        neutral_count = sum(1 for keyword in self.neutral_indicators if keyword in text_lower)
        
        total = left_count + right_count + neutral_count or 1
        
        left_score = left_count / total
        right_score = right_count / total
        neutral_score = neutral_count / total
        
        # Classify bias
        if left_score > right_score and left_score > neutral_score:
            bias_category = 'left_leaning'
            confidence = left_score
        elif right_score > left_score and right_score > neutral_score:
            bias_category = 'right_leaning'
            confidence = right_score
        else:
            bias_category = 'neutral'
            confidence = neutral_score
        
        return {
            'left_score': round(left_score, 3),
            'right_score': round(right_score, 3),
            'neutral_score': round(neutral_score, 3),
            'bias_category': bias_category,
            'confidence': round(confidence, 3)
        }
    
    def analyze_journalist_bias(self, journalist: Dict, articles: Optional[List[str]] = None) -> Dict:
        """Analyze bias of a journalist based on their bio and articles"""
        # Analyze bio
        bio = journalist.get('bio', '')
        bio_bias = self.analyze_bias(bio)
        
        # Analyze articles if available
        if articles:
            article_biases = [self.analyze_bias(article) for article in articles]
            
            # Average scores
            avg_left = sum(b['left_score'] for b in article_biases) / len(article_biases)
            avg_right = sum(b['right_score'] for b in article_biases) / len(article_biases)
            avg_neutral = sum(b['neutral_score'] for b in article_biases) / len(article_biases)
            
            # Determine overall category
            if avg_left > avg_right and avg_left > avg_neutral:
                category = 'left_leaning'
                confidence = avg_left
            elif avg_right > avg_left and avg_right > avg_neutral:
                category = 'right_leaning'
                confidence = avg_right
            else:
                category = 'neutral'
                confidence = avg_neutral
            
            return {
                'bio_bias': bio_bias,
                'article_bias': {
                    'left_score': round(avg_left, 3),
                    'right_score': round(avg_right, 3),
                    'neutral_score': round(avg_neutral, 3),
                    'bias_category': category,
                    'confidence': round(confidence, 3)
                },
                'overall_bias': category
            }
        else:
            return {
                'bio_bias': bio_bias,
                'overall_bias': bio_bias['bias_category']
            }
    
    def _neutral_bias(self) -> Dict[str, float]:
        """Return neutral bias scores"""
        return {
            'left_score': 0.0,
            'right_score': 0.0,
            'neutral_score': 1.0,
            'bias_category': 'neutral',
            'confidence': 1.0
        }
    
    def compare_outlet_biases(self, outlets_data: Dict[int, List[Dict]]) -> Dict[int, Dict]:
        """Compare bias across multiple outlets"""
        outlet_biases = {}
        
        for outlet_id, journalists in outlets_data.items():
            biases = [
                self.analyze_bias(j.get('bio', ''))
                for j in journalists
                if j.get('bio')
            ]
            
            if biases:
                avg_left = sum(b['left_score'] for b in biases) / len(biases)
                avg_right = sum(b['right_score'] for b in biases) / len(biases)
                avg_neutral = sum(b['neutral_score'] for b in biases) / len(biases)
                
                outlet_biases[outlet_id] = {
                    'left_score': round(avg_left, 3),
                    'right_score': round(avg_right, 3),
                    'neutral_score': round(avg_neutral, 3),
                    'bias_category': self._classify_outlet_bias(avg_left, avg_right, avg_neutral)
                }
        
        return outlet_biases
    
    def _classify_outlet_bias(self, left: float, right: float, neutral: float) -> str:
        """Classify overall outlet bias"""
        if left > right and left > neutral:
            return 'left_leaning'
        elif right > left and right > neutral:
            return 'right_leaning'
        else:
            return 'neutral'


# Global instance
bias_detector = BiasDetector()
