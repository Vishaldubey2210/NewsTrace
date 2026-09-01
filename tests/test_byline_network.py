from app.analytics.byline_network import byline_network_builder

def test_byline_network():
    arts = [{'authors': ['Alice', 'Bob']}]
    pairs = byline_network_builder.build_pairs(arts)
    assert len(pairs) == 1
