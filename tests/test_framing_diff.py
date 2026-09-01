from app.analytics.framing_diff import framing_diff_analyzer

def test_framing_diff():
    res = framing_diff_analyzer.compare_framing(['jobs', 'growth'], ['layoffs', 'recession'])
    assert 'jobs' in res['outlet_1_emphasis']
    assert 'layoffs' in res['outlet_2_emphasis']
