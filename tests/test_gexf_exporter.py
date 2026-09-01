from app.export.gexf_exporter import gexf_exporter

def test_gexf_exporter():
    res = gexf_exporter.export([], [])
    assert "<gexf" in res
