"""
Scraper Factory
Dynamically resolves appropriate scraping strategy based on target domain and content dynamism.
"""

from app.scrapers.bs4_scraper import BS4Scraper
from app.scrapers.playwright_scraper import PlaywrightScraper
from app.scrapers.website_detector import WebsiteDetector

class ScraperFactory:
    """Factory provider returning the optimal scraper implementation."""

    def __init__(self):
        self.bs4_scraper = BS4Scraper()
        self.playwright_scraper = PlaywrightScraper()
        self.detector = WebsiteDetector()

    def get_scraper(self, url: str):
        """Determines whether to use standard parser or dynamic browser."""
        site_info = self.detector.detect_type(url)
        if site_info.get("requires_js", False):
            return self.playwright_scraper
        return self.bs4_scraper

    def scrape(self, url: str):
        """Convenience unified scraping entrypoint."""
        scraper = self.get_scraper(url)
        if isinstance(scraper, BS4Scraper):
            return scraper.scrape_url(url)
        else:
            import asyncio
            return asyncio.run(scraper.scrape_dynamic_url(url))
