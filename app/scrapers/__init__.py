"""
NewsTrace Scrapers Module
Web scraping initialization
"""

from app.scrapers.website_detector import website_detector
from app.scrapers.utils import scraper_utils

__all__ = [
    'website_detector',
    'scraper_utils'
]
