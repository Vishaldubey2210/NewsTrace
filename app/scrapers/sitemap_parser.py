import xml.etree.ElementTree as ET
import requests

class SitemapParser:
    """Fetches and parses sitemap.xml for fast URL indexing"""
    def fetch_article_urls(self, sitemap_url, limit=30):
        urls = []
        try:
            resp = requests.get(sitemap_url, timeout=5)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for elem in root.findall('.//{*}loc'):
                    if elem.text:
                        urls.append(elem.text.strip())
                        if len(urls) >= limit: break
        except Exception:
            pass
        return urls

sitemap_parser = SitemapParser()
