class ExcelExporter:
    """Exports tabular data to CSV"""
    def export(self, rows):
        return "ID,Name,Beat\n"

excel_exporter = ExcelExporter()
