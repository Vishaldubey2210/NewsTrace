from app.export.html_report_generator import html_report_generator

def test_html_report():
    html = html_report_generator.generate_html({'name': 'BBC'})
    assert "BBC" in html
