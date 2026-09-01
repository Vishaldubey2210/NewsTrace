from app.export.epub_exporter import markdown_brief_exporter

def test_markdown_brief():
    md = markdown_brief_exporter.export({'name': 'Reuters'})
    assert "Reuters" in md
