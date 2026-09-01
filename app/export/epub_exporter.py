class MarkdownBriefExporter:
    """Generates Markdown briefing"""
    def export(self, outlet):
        return f"# Brief: {outlet.get('name')}"

markdown_brief_exporter = MarkdownBriefExporter()
