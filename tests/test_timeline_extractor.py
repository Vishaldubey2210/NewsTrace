from app.analytics.timeline_extractor import timeline_extractor

def test_timeline_extraction():
    articles = [{'title': 'Major treaty signed in 2021 during summit'}]
    timeline = timeline_extractor.extract_timeline(articles)
    assert len(timeline) == 1
    assert timeline[0]['year'] == 2021
