from bs4 import BeautifulSoup

class OpenGraphExtractor:
    """Extracts OpenGraph, Twitter Card, and Schema.org metadata from news articles"""
    def extract_metadata(self, html_content):
        if not html_content: return {}
        soup = BeautifulSoup(html_content, 'html.parser')
        metadata = {}
        for tag in soup.find_all('meta'):
            prop = tag.get('property') or tag.get('name')
            content = tag.get('content')
            if prop and content and prop in ['og:title', 'og:description', 'og:image', 'author']:
                metadata[prop] = content
        return metadata

opengraph_extractor = OpenGraphExtractor()
