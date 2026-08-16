"""Unit tests for HTML parsers and scraper factory."""
from app.scrapers.bs4_scraper import BS4Scraper
from app.scrapers.scraper_factory import ScraperFactory

def test_bs4_html_parsing():
    scraper = BS4Scraper()
    sample_html = """
    <html>
        <head><title>Breaking News Headline</title></head>
        <body>
            <h1>Breaking News Headline</h1>
            <p>This is the first comprehensive paragraph of the breaking news event.</p>
            <p>The second paragraph gives more context and factual statements.</p>
        </body>
    </html>
    """
    res = scraper.parse_html(sample_html, "http://example.com/news")
    assert res["title"] == "Breaking News Headline"
    assert "breaking news event" in res["content"]
    assert res["success"] is True

def test_scraper_factory():
    factory = ScraperFactory()
    scraper = factory.get_scraper("http://example.com/news")
    assert scraper is not None
