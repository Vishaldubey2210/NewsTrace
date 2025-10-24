# Placeholder file
"""
NewsTrace Database Models
SQLite ORM models using dataclasses
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List
import json


@dataclass
class Outlet:
    """News outlet model"""
    id: Optional[int] = None
    name: str = ""
    official_url: Optional[str] = None
    domain: Optional[str] = None
    detected_at: datetime = field(default_factory=datetime.now)
    last_scraped: Optional[datetime] = None
    total_journalists: int = 0
    status: str = "active"
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'official_url': self.official_url,
            'domain': self.domain,
            'detected_at': self.detected_at.isoformat() if self.detected_at else None,
            'last_scraped': self.last_scraped.isoformat() if self.last_scraped else None,
            'total_journalists': self.total_journalists,
            'status': self.status,
            'metadata': self.metadata
        }


@dataclass
class Journalist:
    """Journalist profile model"""
    id: Optional[int] = None
    name: str = ""
    outlet_id: int = 0
    beat: Optional[str] = None
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    bio: Optional[str] = None
    profile_url: Optional[str] = None
    twitter_handle: Optional[str] = None
    linkedin_url: Optional[str] = None
    first_seen: datetime = field(default_factory=datetime.now)
    last_updated: datetime = field(default_factory=datetime.now)
    article_count: int = 0
    influence_score: float = 0.0
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'outlet_id': self.outlet_id,
            'beat': self.beat,
            'contact_email': self.contact_email,
            'contact_phone': self.contact_phone,
            'bio': self.bio,
            'profile_url': self.profile_url,
            'twitter_handle': self.twitter_handle,
            'linkedin_url': self.linkedin_url,
            'first_seen': self.first_seen.isoformat() if self.first_seen else None,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'article_count': self.article_count,
            'influence_score': self.influence_score,
            'metadata': self.metadata
        }


@dataclass
class Article:
    """Article model"""
    id: Optional[int] = None
    journalist_id: int = 0
    outlet_id: int = 0
    title: str = ""
    url: Optional[str] = None
    published_date: Optional[datetime] = None
    category: Optional[str] = None
    keywords: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    word_count: Optional[int] = None
    scraped_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'journalist_id': self.journalist_id,
            'outlet_id': self.outlet_id,
            'title': self.title,
            'url': self.url,
            'published_date': self.published_date.isoformat() if self.published_date else None,
            'category': self.category,
            'keywords': self.keywords,
            'sentiment_score': self.sentiment_score,
            'word_count': self.word_count,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None
        }


@dataclass
class Topic:
    """Topic model for topic modeling"""
    id: Optional[int] = None
    name: str = ""
    keywords: List[str] = field(default_factory=list)
    article_count: int = 0
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'keywords': self.keywords,
            'article_count': self.article_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@dataclass
class ScrapingJob:
    """Scraping job tracking model"""
    id: Optional[int] = None
    outlet_name: str = ""
    status: str = "pending"  # pending, running, completed, failed
    profiles_found: int = 0
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    metadata: dict = field(default_factory=dict)
    
    def to_dict(self):
        """Convert to dictionary"""
        return {
            'id': self.id,
            'outlet_name': self.outlet_name,
            'status': self.status,
            'profiles_found': self.profiles_found,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'error_message': self.error_message,
            'metadata': self.metadata
        }
