class HTMLReportGenerator:
    """Generates standalone HTML report"""
    def generate_html(self, outlet):
        return f"<html><body><h1>Report: {outlet.get('name')}</h1></body></html>"

html_report_generator = HTMLReportGenerator()
