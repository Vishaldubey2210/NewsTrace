"""
NewsTrace Entity Extractor
Extract journalist beats and topics using spaCy
"""

import logging
from typing import List, Dict, Set
import re

logger = logging.getLogger(__name__)

# Try to load spaCy model
try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    SPACY_AVAILABLE = True
except:
    SPACY_AVAILABLE = False
    logger.warning("[WARN] spaCy model not available - using fallback")


class EntityExtractor:
    """Extract entities and topics from text"""
    
    def __init__(self):
        self.spacy_available = SPACY_AVAILABLE
        
        # Predefined news topics/beats
        self.topic_keywords = {
            'Politics': ['election', 'government', 'parliament', 'minister', 'politics', 'democracy', 'vote', 'policy'],
            'Business': ['economy', 'market', 'stock', 'finance', 'company', 'corporate', 'trade', 'investment'],
            'Technology': ['tech', 'software', 'digital', 'ai', 'startup', 'innovation', 'internet', 'app'],
            'Sports': ['cricket', 'football', 'olympic', 'tournament', 'player', 'match', 'game', 'sport'],
            'Entertainment': ['film', 'movie', 'actor', 'music', 'celebrity', 'bollywood', 'hollywood', 'entertainment'],
            'Health': ['health', 'medical', 'hospital', 'doctor', 'disease', 'pandemic', 'healthcare', 'wellness'],
            'Science': ['science', 'research', 'study', 'scientist', 'discovery', 'experiment', 'space', 'climate'],
            'Education': ['education', 'school', 'university', 'student', 'exam', 'learning', 'academic', 'teacher'],
            'International': ['international', 'global', 'foreign', 'world', 'country', 'diplomatic', 'embassy'],
            'Crime': ['crime', 'police', 'arrest', 'court', 'justice', 'law', 'investigation', 'murder'],
        }
    
    def extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        detected_topics = []
        
        # Match against predefined topics
        for topic, keywords in self.topic_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_topics.append(topic)
                    break
        
        return list(set(detected_topics))  # Remove duplicates
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        entities = {
            'persons': [],
            'organizations': [],
            'locations': [],
            'topics': []
        }
        
        if not text:
            return entities
        
        # Extract topics first
        entities['topics'] = self.extract_topics(text)
        
        # If spaCy available, extract entities
        if self.spacy_available:
            try:
                doc = nlp(text[:1000])  # Limit text length
                
                for ent in doc.ents:
                    if ent.label_ == 'PERSON':
                        entities['persons'].append(ent.text)
                    elif ent.label_ == 'ORG':
                        entities['organizations'].append(ent.text)
                    elif ent.label_ in ['GPE', 'LOC']:
                        entities['locations'].append(ent.text)
                
                # Remove duplicates
                entities['persons'] = list(set(entities['persons']))
                entities['organizations'] = list(set(entities['organizations']))
                entities['locations'] = list(set(entities['locations']))
                
            except Exception as e:
                logger.error(f"[ERROR] Entity extraction failed: {e}")
        
        return entities
    
    def infer_beat_from_bio(self, bio: str) -> str:
        """Infer journalist beat from bio"""
        if not bio:
            return "General"
        
        topics = self.extract_topics(bio)
        
        if topics:
            return topics[0]  # Return primary topic
        
        return "General"


# Global instance
entity_extractor = EntityExtractor()
