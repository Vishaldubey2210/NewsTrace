import random

class HeaderRotator:
    """Provides randomized browser request headers"""
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/121.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/119.0"
    ]
    def get_headers(self):
        return {'User-Agent': random.choice(self.USER_AGENTS), 'Accept': 'text/html'}

header_rotator = HeaderRotator()
