# Placeholder file
"""
NewsTrace Scraping Utilities
Helper functions for web scraping
"""

import random
import time
import logging
from typing import Optional
from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser
from fake_useragent import UserAgent

logger = logging.getLogger(__name__)


class ScraperUtils:
    """Scraping utility functions"""
    
    def __init__(self):
        """Initialize scraper utils"""
        try:
            self.ua = UserAgent()
        except:
            self.ua = None
        
        self.default_user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
    
    def get_random_user_agent(self) -> str:
        """Get random user agent"""
        try:
            if self.ua:
                return self.ua.random
        except:
            pass
        
        return random.choice(self.default_user_agents)
    
    def check_robots_txt(self, url: str, user_agent: str = '*') -> bool:
        """
        Check if URL is allowed by robots.txt
        
        Args:
            url: URL to check
            user_agent: User agent string
            
        Returns:
            True if allowed, False if disallowed
        """
        try:
            parsed = urlparse(url)
            robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
            
            rp = RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            
            return rp.can_fetch(user_agent, url)
        except Exception as e:
            logger.warning(f"Could not check robots.txt: {e}")
            return True  # Allow if robots.txt unavailable
    
    def respectful_delay(self, min_delay: int = 1, max_delay: int = 3):
        """Add respectful delay between requests"""
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    def extract_domain(self, url: str) -> str:
        """Extract domain from URL"""
        try:
            return urlparse(url).netloc
        except:
            return ""
    
    def is_valid_journalist_profile(self, data: dict) -> bool:
        """Validate journalist profile data"""
        required_fields = ['name']
        
        # Check required fields
        if not all(data.get(field) for field in required_fields):
            return False
        
        # Check name length
        name = data.get('name', '')
        if len(name) < 3 or len(name) > 100:
            return False
        
        return True


# Global instance
scraper_utils = ScraperUtils()
