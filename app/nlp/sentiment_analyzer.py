"""
NewsTrace Sentiment Analyzer
Analyze sentiment of journalist bios and articles using TextBlob
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

# Try to import TextBlob
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    logger.warning("[WARN] TextBlob not available - install with: pip install textblob")


class SentimentAnalyzer:
    """Analyze sentiment of text content"""
    
    def __init__(self):
        self.available = TEXTBLOB_AVAILABLE
        if self.available:
            logger.info("[OK] SentimentAnalyzer initialized with TextBlob")
        else:
            logger.info("[INFO] SentimentAnalyzer in fallback mode")
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            
        Returns:
            {
                'polarity': float (-1 to 1),
                'subjectivity': float (0 to 1),
                'sentiment': str ('positive', 'negative', 'neutral')
            }
        """
        if not text or not text.strip():
            return self._neutral_sentiment()
        
        if not self.available:
            return self._fallback_sentiment(text)
        
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = 'positive'
            elif polarity < -0.1:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'
            
            return {
                'polarity': round(polarity, 3),
                'subjectivity': round(subjectivity, 3),
                'sentiment': sentiment,
                'confidence': abs(polarity)
            }
            
        except Exception as e:
            logger.error(f"[ERROR] Sentiment analysis failed: {e}")
            return self._neutral_sentiment()
    
    def analyze_bio_sentiment(self, journalist_data: Dict) -> Dict:
        """Analyze sentiment of journalist bio"""
        bio = journalist_data.get('bio', '')
        
        if bio:
            sentiment = self.analyze_sentiment(bio)
            journalist_data['sentiment'] = sentiment
        else:
            journalist_data['sentiment'] = self._neutral_sentiment()
        
        return journalist_data
    
    def _fallback_sentiment(self, text: str) -> Dict[str, float]:
        """Simple keyword-based fallback sentiment"""
        text_lower = text.lower()
        
        positive_words = ['excellent', 'good', 'great', 'amazing', 'best', 'outstanding', 'positive']
        negative_words = ['bad', 'poor', 'worst', 'terrible', 'negative', 'awful']
        
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            polarity = 0.5
            sentiment = 'positive'
        elif neg_count > pos_count:
            polarity = -0.5
            sentiment = 'negative'
        else:
            polarity = 0.0
            sentiment = 'neutral'
        
        return {
            'polarity': polarity,
            'subjectivity': 0.5,
            'sentiment': sentiment,
            'confidence': 0.3
        }
    
    def _neutral_sentiment(self) -> Dict[str, float]:
        """Return neutral sentiment"""
        return {
            'polarity': 0.0,
            'subjectivity': 0.0,
            'sentiment': 'neutral',
            'confidence': 0.0
        }


# Global instance
sentiment_analyzer = SentimentAnalyzer()
