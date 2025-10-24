"""
NewsTrace Cross-Outlet Tracker
Detect same journalists across multiple news outlets using fuzzy matching
"""

import logging
from typing import List, Dict, Set, Tuple
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

# Try to import fuzzywuzzy for better matching
try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    logger.warning("[WARN] fuzzywuzzy not available - using basic matching")


class CrossOutletTracker:
    """Track journalists across multiple outlets"""
    
    def __init__(self, similarity_threshold: float = 0.85):
        self.similarity_threshold = similarity_threshold
        self.use_fuzzy = FUZZYWUZZY_AVAILABLE
    
    def find_cross_outlet_journalists(self, outlets_data: Dict[int, List[Dict]]) -> List[Dict]:
        """
        Find journalists appearing in multiple outlets
        
        Args:
            outlets_data: {outlet_id: [journalist_dicts]}
            
        Returns:
            List of cross-outlet matches with metadata
        """
        matches = []
        
        # Get all journalists with outlet info
        all_journalists = []
        for outlet_id, journalists in outlets_data.items():
            for journalist in journalists:
                all_journalists.append({
                    **journalist,
                    'source_outlet_id': outlet_id
                })
        
        # Compare all pairs
        seen_pairs = set()
        
        for i, j1 in enumerate(all_journalists):
            for j2 in all_journalists[i+1:]:
                # Skip same outlet
                if j1['source_outlet_id'] == j2['source_outlet_id']:
                    continue
                
                # Check if already processed
                pair_key = tuple(sorted([j1['id'], j2['id']]))
                if pair_key in seen_pairs:
                    continue
                
                # Calculate similarity
                similarity = self._calculate_similarity(j1, j2)
                
                if similarity >= self.similarity_threshold:
                    matches.append({
                        'journalist_1': j1,
                        'journalist_2': j2,
                        'similarity_score': round(similarity, 3),
                        'match_type': self._classify_match(similarity),
                        'common_fields': self._get_common_fields(j1, j2)
                    })
                    seen_pairs.add(pair_key)
        
        logger.info(f"[CROSS-OUTLET] Found {len(matches)} cross-outlet matches")
        return matches
    
    def _calculate_similarity(self, j1: Dict, j2: Dict) -> float:
        """Calculate similarity between two journalists"""
        scores = []
        
        # Name similarity (most important)
        name_sim = self._string_similarity(
            j1.get('name', ''),
            j2.get('name', '')
        )
        scores.append(name_sim * 0.6)  # 60% weight
        
        # Email similarity
        if j1.get('contact_email') and j2.get('contact_email'):
            email_sim = self._string_similarity(
                j1['contact_email'],
                j2['contact_email']
            )
            scores.append(email_sim * 0.2)  # 20% weight
        
        # Beat similarity
        if j1.get('beat') and j2.get('beat'):
            beat_sim = 1.0 if j1['beat'] == j2['beat'] else 0.5
            scores.append(beat_sim * 0.1)  # 10% weight
        
        # Twitter handle similarity
        if j1.get('twitter_handle') and j2.get('twitter_handle'):
            twitter_sim = self._string_similarity(
                j1['twitter_handle'],
                j2['twitter_handle']
            )
            scores.append(twitter_sim * 0.1)  # 10% weight
        
        return sum(scores) / len(scores) if scores else 0.0
    
    def _string_similarity(self, str1: str, str2: str) -> float:
        """Calculate string similarity"""
        if not str1 or not str2:
            return 0.0
        
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        if str1 == str2:
            return 1.0
        
        if self.use_fuzzy:
            return fuzz.ratio(str1, str2) / 100.0
        else:
            return SequenceMatcher(None, str1, str2).ratio()
    
    def _classify_match(self, similarity: float) -> str:
        """Classify match confidence"""
        if similarity >= 0.95:
            return 'exact'
        elif similarity >= 0.85:
            return 'high_confidence'
        elif similarity >= 0.75:
            return 'medium_confidence'
        else:
            return 'low_confidence'
    
    def _get_common_fields(self, j1: Dict, j2: Dict) -> List[str]:
        """Get list of matching fields"""
        common = []
        
        fields_to_check = ['name', 'contact_email', 'beat', 'twitter_handle', 'linkedin_url']
        
        for field in fields_to_check:
            if j1.get(field) and j2.get(field):
                if self._string_similarity(str(j1[field]), str(j2[field])) > 0.8:
                    common.append(field)
        
        return common
    
    def group_by_person(self, matches: List[Dict]) -> List[List[Dict]]:
        """Group matches into clusters representing same person"""
        # Build graph of connections
        connections = {}
        
        for match in matches:
            j1_id = match['journalist_1']['id']
            j2_id = match['journalist_2']['id']
            
            if j1_id not in connections:
                connections[j1_id] = set()
            if j2_id not in connections:
                connections[j2_id] = set()
            
            connections[j1_id].add(j2_id)
            connections[j2_id].add(j1_id)
        
        # Find connected components
        visited = set()
        groups = []
        
        for journalist_id in connections:
            if journalist_id not in visited:
                group = self._dfs(journalist_id, connections, visited)
                groups.append(group)
        
        return groups
    
    def _dfs(self, node: int, graph: Dict, visited: Set) -> List[int]:
        """Depth-first search for connected components"""
        visited.add(node)
        component = [node]
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                component.extend(self._dfs(neighbor, graph, visited))
        
        return component


# Global instance
cross_outlet_tracker = CrossOutletTracker(similarity_threshold=0.85)
