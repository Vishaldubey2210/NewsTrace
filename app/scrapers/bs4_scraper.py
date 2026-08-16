"""
BeautifulSoup Web Scraper Module
Provides resilient HTML parsing, article content extraction, and metadata extraction.
"""

import requests
from bs4 import BeautifulSoup
from typing import Dict, Any, Optional
import time

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
}

class BS4Scraper:
    """Extracts structured news articles from standard HTML web pages."""

    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def scrape_url(self, url: str) -> Dict[str, Any]:
        """Fetches and parses a single article URL."""
        try:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            return self.parse_html(response.text, url)
        except Exception as e:
            return {
                "url": url,
                "title": "",
                "content": "",
                "author": "Unknown",
                "publish_date": "",
                "success": False,
                "error": str(e)
            }

    def parse_html(self, html_content: str, url: str = "") -> Dict[str, Any]:
        """Parses raw HTML to extract title, body paragraphs, and meta tags."""
        soup = BeautifulSoup(html_content, 'html.parser')

        # Extract title
        title = ""
        if soup.find('h1'):
            title = soup.find('h1').get_text().strip()
        elif soup.title:
            title = soup.title.get_text().strip()

        # Extract body text
        paragraphs = soup.find_all('p')
        content_paras = [p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 30]
        content = " ".join(content_paras)

        # Extract author
        author = "Unknown"
        author_meta = soup.find('meta', attrs={'name': 'author'}) or soup.find('meta', property='article:author')
        if author_meta and author_meta.get('content'):
            author = author_meta['content'].strip()

        # Extract published date
        date = ""
        date_meta = soup.find('meta', property='article:published_time') or soup.find('meta', attrs={'name': 'date'})
        if date_meta and date_meta.get('content'):
            date = date_meta['content'].strip()

        return {
            "url": url,
            "title": title,
            "content": content,
            "author": author,
            "publish_date": date,
            "success": len(content) > 0,
            "timestamp": time.time()
        }
