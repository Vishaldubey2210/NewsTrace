"""
Playwright Headless Browser Scraper
Handles dynamic Single Page Applications (SPA), client-side JavaScript rendering, and bot protection bypass.
"""

from typing import Dict, Any
from app.scrapers.bs4_scraper import BS4Scraper

class PlaywrightScraper:
    """Renders JavaScript-heavy dynamic news web pages."""

    def __init__(self, headless: bool = True, timeout: int = 15000):
        self.headless = headless
        self.timeout = timeout
        self.bs4_fallback = BS4Scraper()

    async def scrape_dynamic_url(self, url: str) -> Dict[str, Any]:
        """Asynchronously fetches dynamic web page with DOM execution."""
        try:
            from playwright.async_api import async_playwright
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                page = await browser.new_page()
                await page.goto(url, timeout=self.timeout)
                await page.wait_for_load_state('networkidle')
                html = await page.content()
                await browser.close()
                return self.bs4_fallback.parse_html(html, url)
        except Exception as e:
            res = self.bs4_fallback.scrape_url(url)
            res["error_notice"] = f"Playwright skipped, used BS4 fallback: {str(e)}"
            return res
