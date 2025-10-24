"""
NewsTrace Topic Modeler
Perform topic modeling using LDA (Latent Dirichlet Allocation)
"""

import logging
from typing import List, Dict, Tuple

logger = logging.getLogger(__name__)

# Try to import sklearn
try:
    from sklearn.feature_extraction.text import CountVectorizer
    from sklearn.decomposition import LatentDirichletAllocation
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    logger.warning("[WARN] scikit-learn not available for topic modeling")


class TopicModeler:
    """LDA-based topic modeling"""
    
    def __init__(self, n_topics: int = 5):
        self.n_topics = n_topics
        self.available = SKLEARN_AVAILABLE
        self.model = None
        self.vectorizer = None
    
    def fit_transform(self, documents: List[str]) -> Tuple[List[List[Tuple[str, float]]], List[int]]:
        """
        Fit LDA model and extract topics
        
        Args:
            documents: List of text documents
            
        Returns:
            (topics, document_topic_assignments)
            topics: List of [(word, weight), ...]
            document_topic_assignments: Document -> Topic mapping
        """
        if not self.available:
            logger.warning("[WARN] Topic modeling not available - using fallback")
            return self._fallback_topics(documents)
        
        if len(documents) < 2:
            logger.warning("[WARN] Need at least 2 documents for topic modeling")
            return [], []
        
        try:
            # Vectorize documents
            self.vectorizer = CountVectorizer(
                max_features=100,
                stop_words='english',
                min_df=1
            )
            doc_term_matrix = self.vectorizer.fit_transform(documents)
            
            # Fit LDA
            self.model = LatentDirichletAllocation(
                n_components=min(self.n_topics, len(documents)),
                random_state=42,
                max_iter=20
            )
            doc_topics = self.model.fit_transform(doc_term_matrix)
            
            # Extract topics
            topics = self._extract_topics()
            
            # Assign documents to topics
            doc_topic_assignments = doc_topics.argmax(axis=1).tolist()
            
            return topics, doc_topic_assignments
            
        except Exception as e:
            logger.error(f"[ERROR] Topic modeling failed: {e}")
            return self._fallback_topics(documents)
    
    def _extract_topics(self) -> List[List[Tuple[str, float]]]:
        """Extract top words for each topic"""
        if not self.model or not self.vectorizer:
            return []
        
        feature_names = self.vectorizer.get_feature_names_out()
        topics = []
        
        for topic_idx, topic in enumerate(self.model.components_):
            top_indices = topic.argsort()[-10:][::-1]
            top_words = [
                (feature_names[i], float(topic[i]))
                for i in top_indices
            ]
            topics.append(top_words)
        
        return topics
    
    def _fallback_topics(self, documents: List[str]) -> Tuple[List, List]:
        """Simple fallback topic assignment"""
        # Just return empty topics
        return [], list(range(len(documents)))


# Global instance
topic_modeler = TopicModeler(n_topics=5)
