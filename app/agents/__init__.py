"""
NewsTrace Agents Module
Multi-agent system initialization
"""

from app.agents.base_agent import BaseAgent
from app.agents.search_agent import search_agent
from app.agents.scraper_agent import scraper_agent
from app.agents.orchestrator import orchestrator

__all__ = [
    'BaseAgent',
    'search_agent',
    'scraper_agent',
    'orchestrator'
]
