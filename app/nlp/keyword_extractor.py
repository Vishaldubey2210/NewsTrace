"""
NewsTrace Keyword Extractor
Extract keywords using TF-IDF algorithm
"""

import logging
from typing import List, Dict
from collections import Counter
import re

logger = logging.getLogger(__name__)

# Try to import sklearn
try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("[WARN] scikit-learn not available - using fallback")


class KeywordExtractor:
    """Extract keywords from text using TF-IDF"""
    
    def __init__(self):
        self.available = SKLEARN_AVAILABLE
        
        # Common stop words
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
            'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where',
            'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most',
            'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same',
            'so', 'than', 'too', 'very', 's', 't', 'just', 'now'
        }
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Dict[str, float]]:
        """
        Extract top N keywords from text
        
        Args:
            text: Input text
            top_n: Number of keywords to return
            
        Returns:
            List of {'keyword': str, 'score': float}
        """
        if not text or not text.strip():
            return []
        
        if self.available:
            return self._extract_with_tfidf([text], top_n)
        else:
            return self._extract_with_frequency(text, top_n)
    
    def extract_keywords_from_corpus(self, texts: List[str], top_n: int = 10) -> Dict[int, List[Dict]]:
        """Extract keywords from multiple documents"""
        if not texts:
            return {}
        
        if self.available:
            return self._extract_corpus_tfidf(texts, top_n)
        else:
            # Fallback: extract from each text individually
            results = {}
            for i, text in enumerate(texts):
                results[i] = self._extract_with_frequency(text, top_n)
            return results
    
    def _extract_with_tfidf(self, texts: List[str], top_n: int) -> List[Dict[str, float]]:
        """Extract keywords using TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores for first document
            scores = tfidf_matrix[0].toarray().flatten()
            
            # Sort by score
            keyword_scores = sorted(
                zip(feature_names, scores),
                key=lambda x: x[1],
                reverse=True
            )[:top_n]
            
            return [
                {'keyword': keyword, 'score': round(float(score), 3)}
                for keyword, score in keyword_scores
                if score > 0
            ]
            
        except Exception as e:
            logger.error(f"[ERROR] TF-IDF extraction failed: {e}")
            return self._extract_with_frequency(texts[0] if texts else "", top_n)
    
    def _extract_corpus_tfidf(self, texts: List[str], top_n: int) -> Dict[int, List[Dict]]:
        """Extract keywords from corpus using TF-IDF"""
        try:
            vectorizer = TfidfVectorizer(
                max_features=100,
                stop_words='english',
                ngram_range=(1, 2),
                min_df=1
            )
            
            tfidf_matrix = vectorizer.fit_transform(texts)
            feature_names = vectorizer.get_feature_names_out()
            
            results = {}
            for i in range(len(texts)):
                scores = tfidf_matrix[i].toarray().flatten()
                keyword_scores = sorted(
                    zip(feature_names, scores),
                    key=lambda x: x[1],
                    reverse=True
                )[:top_n]
                
                results[i] = [
                    {'keyword': keyword, 'score': round(float(score), 3)}
                    for keyword, score in keyword_scores
                    if score > 0
                ]
            
            return results
            
        except Exception as e:
            logger.error(f"[ERROR] Corpus TF-IDF failed: {e}")
            return {}
    
    def _extract_with_frequency(self, text: str, top_n: int) -> List[Dict[str, float]]:
        """Fallback: Extract keywords by frequency"""
        # Clean text
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filter stop words and short words
        filtered_words = [
            word for word in words
            if word not in self.stop_words and len(word) > 3
        ]
        
        # Count frequencies
        word_counts = Counter(filtered_words)
        
        # Normalize scores
        max_count = max(word_counts.values()) if word_counts else 1
        
        top_words = word_counts.most_common(top_n)
        
        return [
            {
                'keyword': word,
                'score': round(count / max_count, 3)
            }
            for word, count in top_words
        ]


# Global instance
keyword_extractor = KeywordExtractor()
