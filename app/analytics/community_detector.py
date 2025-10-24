"""
NewsTrace Community Detector
Detect journalist communities/clusters using graph algorithms
"""

import logging
from typing import List, Dict, Set
import networkx as nx

logger = logging.getLogger(__name__)


class CommunityDetector:
    """Detect communities in journalist networks"""
    
    def __init__(self):
        self.graph = None
    
    def detect_communities(self, journalists: List[Dict], edges: List[Tuple[int, int]]) -> Dict[int, int]:
        """
        Detect communities using Louvain algorithm
        
        Args:
            journalists: List of journalist data
            edges: List of (journalist_id1, journalist_id2) connections
            
        Returns:
            {journalist_id: community_id}
        """
        # Build graph
        G = nx.Graph()
        
        # Add nodes
        for journalist in journalists:
            G.add_node(journalist['id'], data=journalist)
        
        # Add edges
        G.add_edges_from(edges)
        
        logger.info(f"[COMMUNITY] Graph: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
        
        # Detect communities
        try:
            # Try Louvain (if available)
            communities = self._louvain_communities(G)
        except:
            # Fallback to simple clustering
            communities = self._simple_clustering(G)
        
        logger.info(f"[COMMUNITY] Detected {len(set(communities.values()))} communities")
        return communities
    
    def _louvain_communities(self, G: nx.Graph) -> Dict[int, int]:
        """Louvain community detection"""
        try:
            import community as community_louvain
            partition = community_louvain.best_partition(G)
            return partition
        except ImportError:
            logger.warning("[WARN] python-louvain not available")
            return self._simple_clustering(G)
    
    def _simple_clustering(self, G: nx.Graph) -> Dict[int, int]:
        """Simple clustering based on connected components"""
        communities = {}
        
        # Get connected components
        for i, component in enumerate(nx.connected_components(G)):
            for node in component:
                communities[node] = i
        
        return communities
    
    def get_community_stats(self, communities: Dict[int, int], journalists: List[Dict]) -> List[Dict]:
        """Get statistics for each community"""
        community_data = {}
        
        # Group journalists by community
        for journalist in journalists:
            j_id = journalist['id']
            comm_id = communities.get(j_id, -1)
            
            if comm_id not in community_data:
                community_data[comm_id] = {
                    'id': comm_id,
                    'members': [],
                    'beats': set(),
                    'outlets': set()
                }
            
            community_data[comm_id]['members'].append(journalist)
            
            if journalist.get('beat'):
                community_data[comm_id]['beats'].add(journalist['beat'])
            
            if journalist.get('outlet_id'):
                community_data[comm_id]['outlets'].add(journalist['outlet_id'])
        
        # Convert to list with stats
        stats = []
        for comm_id, data in community_data.items():
            stats.append({
                'community_id': comm_id,
                'size': len(data['members']),
                'beats': list(data['beats']),
                'outlets': list(data['outlets']),
                'top_members': data['members'][:5]  # Top 5 members
            })
        
        return sorted(stats, key=lambda x: x['size'], reverse=True)
    
    def find_influencers(self, G: nx.Graph, top_n: int = 10) -> List[Dict]:
        """Find most influential journalists using centrality metrics"""
        influencers = []
        
        if G.number_of_nodes() == 0:
            return influencers
        
        try:
            # Calculate centrality metrics
            degree_centrality = nx.degree_centrality(G)
            betweenness_centrality = nx.betweenness_centrality(G)
            
            # Combine scores
            combined_scores = {}
            for node in G.nodes():
                combined_scores[node] = (
                    degree_centrality.get(node, 0) * 0.6 +
                    betweenness_centrality.get(node, 0) * 0.4
                )
            
            # Get top influencers
            top_nodes = sorted(
                combined_scores.items(),
                key=lambda x: x[1],
                reverse=True
            )[:top_n]
            
            for node, score in top_nodes:
                node_data = G.nodes[node].get('data', {})
                influencers.append({
                    'journalist_id': node,
                    'name': node_data.get('name', 'Unknown'),
                    'influence_score': round(score, 3),
                    'degree': G.degree(node),
                    'data': node_data
                })
        
        except Exception as e:
            logger.error(f"[ERROR] Influencer detection failed: {e}")
        
        return influencers


# Global instance
community_detector = CommunityDetector()
