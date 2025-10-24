"""
NewsTrace Graph Builder - FIXED VERSION
Build NetworkX graph for journalist-topic relationships with comprehensive error handling
"""

import logging
from typing import List, Dict, Optional
import networkx as nx
import json

logger = logging.getLogger(__name__)


class GraphBuilder:
    """Build and analyze journalist network graphs"""
    
    def __init__(self):
        self.graph = None
    
    def build_bipartite_graph(self, journalists: List[Dict], topics: List[str]) -> nx.Graph:
        """
        Build bipartite graph of journalists and topics with full error handling
        
        Args:
            journalists: List of journalist dictionaries
            topics: List of all unique topics
            
        Returns:
            NetworkX Graph object
        """
        G = nx.Graph()
        
        # Safety check
        if not journalists:
            logger.warning("[GRAPH] No journalists data provided")
            return G
        
        if not topics:
            logger.warning("[GRAPH] No topics provided, will extract from journalists")
            topics = []
        
        logger.info(f"[GRAPH] Building graph for {len(journalists)} journalists")
        
        # Track added nodes
        added_journalists = 0
        added_topics = set()
        added_edges = 0
        
        # Add journalist nodes and their topic relationships
        for journalist in journalists:
            try:
                # Get journalist name safely
                j_name = journalist.get('name')
                if not j_name:
                    logger.warning(f"[GRAPH] Skipping journalist without name: {journalist}")
                    continue
                
                # Add journalist node
                G.add_node(
                    j_name,
                    node_type='journalist',
                    bipartite=0,
                    data=journalist
                )
                added_journalists += 1
                
                # Extract topics from journalist data
                j_topics = self._extract_topics_from_journalist(journalist)
                
                # Add topic nodes and edges
                for topic in j_topics:
                    if topic and isinstance(topic, str) and topic.strip():
                        topic = topic.strip()
                        
                        # Add topic node if not exists
                        if not G.has_node(topic):
                            G.add_node(
                                topic,
                                node_type='topic',
                                bipartite=1
                            )
                            added_topics.add(topic)
                        
                        # Add edge between journalist and topic
                        if not G.has_edge(j_name, topic):
                            G.add_edge(j_name, topic)
                            added_edges += 1
                
            except Exception as e:
                logger.error(f"[GRAPH] Error processing journalist {journalist.get('name', 'Unknown')}: {e}")
                continue
        
        logger.info(f"[GRAPH] Built graph successfully:")
        logger.info(f"  - Journalists: {added_journalists}")
        logger.info(f"  - Topics: {len(added_topics)}")
        logger.info(f"  - Edges: {added_edges}")
        logger.info(f"  - Total nodes: {G.number_of_nodes()}")
        logger.info(f"  - Total edges: {G.number_of_edges()}")
        
        self.graph = G
        return G
    
    def _extract_topics_from_journalist(self, journalist: Dict) -> List[str]:
        """
        Extract topics from journalist data with multiple fallback strategies
        
        Args:
            journalist: Journalist dictionary
            
        Returns:
            List of topic strings
        """
        topics = []
        
        try:
            # Strategy 1: Get from metadata.topics
            metadata = journalist.get('metadata')
            
            if metadata:
                # Handle string metadata (JSON)
                if isinstance(metadata, str):
                    try:
                        metadata = json.loads(metadata)
                    except json.JSONDecodeError:
                        logger.warning(f"[GRAPH] Could not parse metadata JSON for {journalist.get('name')}")
                        metadata = {}
                
                # Extract topics from metadata dict
                if isinstance(metadata, dict):
                    meta_topics = metadata.get('topics', [])
                    
                    if meta_topics:
                        if isinstance(meta_topics, list):
                            topics.extend([str(t) for t in meta_topics if t])
                        elif isinstance(meta_topics, str):
                            topics.append(meta_topics)
            
            # Strategy 2: Use beat as topic
            beat = journalist.get('beat')
            if beat and isinstance(beat, str) and beat.strip():
                beat = beat.strip()
                if beat not in topics:
                    topics.append(beat)
            
            # Strategy 3: Extract from bio keywords (optional)
            if not topics:
                bio = journalist.get('bio', '')
                if bio:
                    # Simple keyword extraction from bio
                    common_beats = ['Politics', 'Sports', 'Technology', 'Business', 
                                   'Entertainment', 'Science', 'Health', 'Education']
                    for keyword in common_beats:
                        if keyword.lower() in bio.lower():
                            topics.append(keyword)
                            break  # Just take first match
            
            # Fallback: Use 'General' if no topics found
            if not topics:
                topics.append('General')
            
        except Exception as e:
            logger.error(f"[GRAPH] Error extracting topics for {journalist.get('name', 'Unknown')}: {e}")
            topics = ['General']  # Fallback
        
        # Clean and deduplicate
        topics = list(set([t.strip() for t in topics if t and isinstance(t, str) and t.strip()]))
        
        return topics
    
    def export_graph_json(self, G: Optional[nx.Graph] = None) -> Dict:
        """
        Export graph to JSON format for Vis.js visualization
        
        Args:
            G: NetworkX Graph (optional, uses self.graph if not provided)
            
        Returns:
            Dictionary with nodes, edges, and stats
        """
        if G is None:
            G = self.graph
        
        if G is None or G.number_of_nodes() == 0:
            logger.warning("[GRAPH] Empty graph, returning empty export")
            return {
                'nodes': [],
                'edges': [],
                'stats': {
                    'total_nodes': 0,
                    'total_edges': 0,
                    'journalist_count': 0,
                    'topic_count': 0
                }
            }
        
        try:
            nodes = []
            edges = []
            
            journalist_count = 0
            topic_count = 0
            
            # Export nodes
            for node_id, node_data in G.nodes(data=True):
                node_type = node_data.get('node_type', 'unknown')
                
                # Determine color and size based on type
                if node_type == 'journalist':
                    color = '#667eea'  # Blue for journalists
                    size = 20
                    journalist_count += 1
                elif node_type == 'topic':
                    color = '#f093fb'  # Pink for topics
                    size = 15
                    topic_count += 1
                else:
                    color = '#4facfe'  # Cyan for others
                    size = 15
                
                nodes.append({
                    'id': str(node_id),
                    'label': str(node_id),
                    'group': node_type,
                    'color': color,
                    'size': size,
                    'title': f'{node_type.title()}: {node_id}'  # Tooltip
                })
            
            # Export edges
            for source, target in G.edges():
                edges.append({
                    'from': str(source),
                    'to': str(target),
                    'color': {'color': 'rgba(255,255,255,0.3)'}
                })
            
            logger.info(f"[GRAPH] Exported {len(nodes)} nodes and {len(edges)} edges")
            
            return {
                'nodes': nodes,
                'edges': edges,
                'stats': {
                    'total_nodes': len(nodes),
                    'total_edges': len(edges),
                    'journalist_count': journalist_count,
                    'topic_count': topic_count
                }
            }
            
        except Exception as e:
            logger.error(f"[GRAPH] Export failed: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return {
                'nodes': [],
                'edges': [],
                'stats': {
                    'total_nodes': 0,
                    'total_edges': 0,
                    'journalist_count': 0,
                    'topic_count': 0
                }
            }
    
    def calculate_centrality(self, G: Optional[nx.Graph] = None) -> Dict[str, float]:
        """
        Calculate node centrality scores (importance in network)
        
        Args:
            G: NetworkX Graph (optional, uses self.graph if not provided)
            
        Returns:
            Dictionary mapping node IDs to centrality scores
        """
        if G is None:
            G = self.graph
        
        if G is None or G.number_of_nodes() == 0:
            logger.warning("[GRAPH] Cannot calculate centrality for empty graph")
            return {}
        
        try:
            # Degree centrality (number of connections)
            centrality = nx.degree_centrality(G)
            
            logger.info(f"[GRAPH] Calculated centrality for {len(centrality)} nodes")
            
            return centrality
            
        except Exception as e:
            logger.error(f"[GRAPH] Centrality calculation failed: {e}")
            return {}
    
    def get_node_neighbors(self, node_id: str, G: Optional[nx.Graph] = None) -> List[str]:
        """
        Get all neighbors of a node
        
        Args:
            node_id: Node identifier
            G: NetworkX Graph (optional)
            
        Returns:
            List of neighbor node IDs
        """
        if G is None:
            G = self.graph
        
        if G is None:
            return []
        
        try:
            if G.has_node(node_id):
                return list(G.neighbors(node_id))
            return []
        except Exception as e:
            logger.error(f"[GRAPH] Error getting neighbors: {e}")
            return []
    
    def get_graph_stats(self, G: Optional[nx.Graph] = None) -> Dict:
        """
        Get comprehensive graph statistics
        
        Args:
            G: NetworkX Graph (optional)
            
        Returns:
            Dictionary with various stats
        """
        if G is None:
            G = self.graph
        
        if G is None or G.number_of_nodes() == 0:
            return {
                'nodes': 0,
                'edges': 0,
                'density': 0,
                'connected_components': 0
            }
        
        try:
            stats = {
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'density': nx.density(G),
                'connected_components': nx.number_connected_components(G)
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"[GRAPH] Stats calculation failed: {e}")
            return {
                'nodes': G.number_of_nodes(),
                'edges': G.number_of_edges(),
                'density': 0,
                'connected_components': 0
            }


# Global instance
graph_builder = GraphBuilder()
