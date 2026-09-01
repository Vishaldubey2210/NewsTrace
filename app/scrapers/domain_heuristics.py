from urllib.parse import urlparse

class DomainHeuristics:
    """Heuristic scoring for author directories"""
    def is_author_url(self, url):
        return any(k in urlparse(url).path.lower() for k in ['/author/', '/writer/', '/by/'])

domain_heuristics = DomainHeuristics()
