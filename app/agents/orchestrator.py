"""
NewsTrace Multi-Agent Orchestrator - ENHANCED
Coordinates agents + NLP + Analytics
"""

from typing import Dict, Any, List
import logging
from datetime import datetime

from app.agents.search_agent import search_agent
from app.agents.scraper_agent import scraper_agent
from app.database.sqlite_db import db_manager
from app.models import Outlet, Journalist
from app.nlp.entity_extractor import entity_extractor
from app.analytics.influence_score import influence_calculator

logger = logging.getLogger(__name__)


class AgentOrchestrator:
    """Enhanced orchestrator with NLP and analytics"""
    
    def __init__(self):
        self.agents = {
            'search': search_agent,
            'scraper': scraper_agent
        }
        logger.info("[AGENT] Enhanced orchestrator initialized")
    
    def profile_outlet(self, outlet_name: str) -> Dict[str, Any]:
        """Complete autonomous profiling workflow with analytics"""
        
        logger.info(f"[START] Autonomous profiling for: {outlet_name}")
        
        workflow_result = {
            'outlet_name': outlet_name,
            'success': False,
            'steps': [],
            'profiles': [],
            'started_at': datetime.now().isoformat()
        }
        
        # Create scraping job
        job_id = db_manager.create_scraping_job(outlet_name)
        
        try:
            # STEP 1: Search Agent - Detect website
            logger.info("[STEP 1] Website Detection")
            search_result = search_agent.run(outlet_name=outlet_name)
            workflow_result['steps'].append(search_result)
            
            if not search_result['success'] or not search_result['result']['found']:
                raise Exception("Website detection failed")
            
            website_info = search_result['result']
            logger.info(f"[OK] Website found: {website_info['url']}")
            
            # Save outlet to database
            outlet = Outlet(
                name=outlet_name,
                official_url=website_info['url'],
                domain=website_info['domain'],
                metadata={'detection_confidence': website_info.get('confidence', 0)}
            )
            outlet_id = db_manager.create_outlet(outlet)
            
            if not outlet_id:
                existing_outlet = db_manager.get_outlet_by_name(outlet_name)
                outlet_id = existing_outlet.id if existing_outlet else None
            
            if not outlet_id:
                raise Exception("Failed to create outlet in database")
            
            # STEP 2: Scraper Agent - Extract profiles
            logger.info("[STEP 2] Profile Extraction")
            scraper_result = scraper_agent.run(
                url=website_info['url'],
                outlet_name=outlet_name
            )
            workflow_result['steps'].append(scraper_result)
            
            if not scraper_result['success']:
                raise Exception("Profile scraping failed")
            
            profiles_data = scraper_result['result']['profiles']
            logger.info(f"[OK] Extracted {len(profiles_data)} profiles")
            
            # STEP 3: NLP Analysis - Extract topics & beats
            logger.info("[STEP 3] NLP Analysis")
            profiles_data = self._enhance_with_nlp(profiles_data)
            
            # STEP 4: Calculate Influence Scores
            logger.info("[STEP 4] Influence Scoring")
            profiles_data = influence_calculator.rank_journalists(profiles_data)
            
            # STEP 5: Save to database
            logger.info("[STEP 5] Saving to Database")
            saved_profiles = self._save_profiles(profiles_data, outlet_id)
            
            # Update outlet statistics
            db_manager.update_outlet_scraped(outlet_id, len(saved_profiles))
            
            # Update scraping job
            db_manager.update_scraping_job(job_id, 'completed', len(saved_profiles))
            
            workflow_result['success'] = True
            workflow_result['profiles'] = saved_profiles
            workflow_result['profile_count'] = len(saved_profiles)
            workflow_result['outlet_id'] = outlet_id
            workflow_result['completed_at'] = datetime.now().isoformat()
            
            logger.info(f"[SUCCESS] Profiling completed: {len(saved_profiles)} journalists")
            
        except Exception as e:
            error_msg = str(e)
            logger.error(f"[ERROR] Workflow failed: {error_msg}")
            
            workflow_result['success'] = False
            workflow_result['error'] = error_msg
            workflow_result['completed_at'] = datetime.now().isoformat()
            
            db_manager.update_scraping_job(job_id, 'failed', 0, error_msg)
        
        return workflow_result
    
    def _enhance_with_nlp(self, profiles: List[Dict]) -> List[Dict]:
        """Enhance profiles with NLP analysis"""
        
        for profile in profiles:
            # Extract topics from bio
            bio = profile.get('bio', '') or ''
            
            if bio:
                topics = entity_extractor.extract_topics(bio)
                profile['topics'] = topics
                
                # Infer beat if not present
                if not profile.get('beat'):
                    profile['beat'] = entity_extractor.infer_beat_from_bio(bio)
            else:
                profile['topics'] = []
                if not profile.get('beat'):
                    profile['beat'] = 'General'
        
        return profiles
    
    def _save_profiles(self, profiles_data: List[Dict], outlet_id: int) -> List[Dict]:
        """Save journalist profiles to database"""
        saved_profiles = []
        
        for profile_data in profiles_data:
            try:
                journalist = Journalist(
                    name=profile_data.get('name'),
                    outlet_id=outlet_id,
                    beat=profile_data.get('beat'),
                    bio=profile_data.get('bio'),
                    contact_email=profile_data.get('contact_email'),
                    contact_phone=profile_data.get('contact_phone'),
                    profile_url=profile_data.get('profile_url'),
                    twitter_handle=profile_data.get('twitter_handle'),
                    linkedin_url=profile_data.get('linkedin_url'),
                    influence_score=profile_data.get('influence_score', 0.0),
                    metadata={
                        'topics': profile_data.get('topics', [])
                    }
                )
                
                journalist_id = db_manager.create_journalist(journalist)
                
                if journalist_id:
                    journalist.id = journalist_id
                    saved_profiles.append(journalist.to_dict())
            
            except Exception as e:
                logger.warning(f"[WARN] Failed to save journalist: {e}")
                continue
        
        return saved_profiles


# Global instance
orchestrator = AgentOrchestrator()
