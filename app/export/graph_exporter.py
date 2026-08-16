"""
Graph Exporter Module
Exports entity network graphs into GEXF, GraphML, Cytoscape, and D3 JSON formats.
"""

import networkx as nx
import json
from typing import Dict, Any

class GraphExporter:
    """Converts NetworkX graph representations into exchangeable graph formats."""

    @staticmethod
    def export_to_d3(graph: nx.Graph) -> Dict[str, Any]:
        """Converts graph into D3.js force-directed graph format."""
        nodes = [{"id": n, "label": n, "degree": graph.degree(n)} for n in graph.nodes()]
        links = [{"source": u, "target": v, "weight": d.get("weight", 1)} for u, v, d in graph.edges(data=True)]
        return {"nodes": nodes, "links": links}

    @staticmethod
    def export_to_gexf(graph: nx.Graph, filepath: str) -> bool:
        """Saves graph as GEXF file for Gephi visualization."""
        try:
            nx.write_gexf(graph, filepath)
            return True
        except Exception:
            return False
