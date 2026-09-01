class GEXFExporter:
    """Exports graph to GEXF"""
    def export(self, nodes, edges):
        return "<gexf><graph></graph></gexf>"

gexf_exporter = GEXFExporter()
