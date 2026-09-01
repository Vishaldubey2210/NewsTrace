from app.export.excel_exporter import excel_exporter

def test_excel_export():
    csv = excel_exporter.export([])
    assert "ID,Name" in csv
