import urllib.parse
import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

class RSSDiscoverer:
    """Auto-discovers RSS / Atom feeds on news websites"""
    COMMON_PATHS = ['/rss', '/feed', '/rss.xml', '/feed.xml']

    def discover_feeds(self, base_url):
        feeds = []
        try:
            resp = requests.get(base_url, headers={'User-Agent': 'NewsTrace/2.0'}, timeout=5)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                for link in soup.find_all('link', type=['application/rss+xml', 'application/atom+xml']):
                    if link.get('href'):
                        feeds.append(urllib.parse.urljoin(base_url, link['href']))
        except Exception:
            pass
        return list(set(feeds))

rss_discoverer = RSSDiscoverer()
