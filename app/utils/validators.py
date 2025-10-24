# Placeholder file
"""
NewsTrace Data Validators
Validation functions for data quality
"""

import re
from typing import Dict, Any, List
import validators as url_validator


def validate_journalist_profile(profile: Dict[str, Any]) -> tuple[bool, List[str]]:
    """
    Validate journalist profile data
    
    Args:
        profile: Journalist profile dictionary
        
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    # Required field: name
    name = profile.get('name', '').strip()
    if not name:
        errors.append("Name is required")
    elif len(name) < 3:
        errors.append("Name too short (minimum 3 characters)")
    elif len(name) > 100:
        errors.append("Name too long (maximum 100 characters)")
    
    # Validate email if provided
    email = profile.get('contact_email', '').strip()
    if email and not validate_email(email):
        errors.append("Invalid email format")
    
    # Validate URLs if provided
    profile_url = profile.get('profile_url', '').strip()
    if profile_url and not url_validator.url(profile_url):
        errors.append("Invalid profile URL")
    
    twitter = profile.get('twitter_handle', '').strip()
    if twitter and not validate_twitter_handle(twitter):
        errors.append("Invalid Twitter handle")
    
    linkedin = profile.get('linkedin_url', '').strip()
    if linkedin and not url_validator.url(linkedin):
        errors.append("Invalid LinkedIn URL")
    
    return (len(errors) == 0, errors)


def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_twitter_handle(handle: str) -> bool:
    """Validate Twitter handle format"""
    # Remove @ if present
    handle = handle.lstrip('@')
    pattern = r'^[A-Za-z0-9_]{1,15}$'
    return bool(re.match(pattern, handle))


def validate_outlet_name(name: str) -> tuple[bool, str]:
    """
    Validate outlet name
    
    Args:
        name: Outlet name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    name = name.strip()
    
    if not name:
        return (False, "Outlet name is required")
    
    if len(name) < 3:
        return (False, "Outlet name too short")
    
    if len(name) > 100:
        return (False, "Outlet name too long")
    
    return (True, "")


def sanitize_text(text: str, max_length: int = None) -> str:
    """
    Sanitize text input
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Sanitized text
    """
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Truncate if needed
    if max_length and len(text) > max_length:
        text = text[:max_length] + '...'
    
    return text
