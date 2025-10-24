"""
NewsTrace SQLite Database Operations - COMPLETE FIXED VERSION
CRUD operations and database initialization with all methods
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from contextlib import contextmanager
import logging

from config import Config
from app.models import Outlet, Journalist, Article, Topic, ScrapingJob

logger = logging.getLogger(__name__)


class DatabaseManager:
    """SQLite database manager with full CRUD operations"""
    
    def __init__(self, db_path: str = None):
        """Initialize database manager"""
        self.db_path = db_path or Config.DATABASE_PATH
        self.schema_path = Path(__file__).parent / 'schema.sql'
        
        # Ensure database directory exists
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database error: {e}")
            raise
        finally:
            conn.close()
    
    def init_database(self):
        """Initialize database with schema"""
        try:
            # Read schema file
            if not self.schema_path.exists():
                logger.error(f"Schema file not found: {self.schema_path}")
                return False
            
            with open(self.schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            
            # Execute schema
            with self.get_connection() as conn:
                conn.executescript(schema_sql)
            
            logger.info("✅ Database initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize database: {e}")
            return False
    
    # ==================== OUTLET OPERATIONS ====================
    
    def create_outlet(self, outlet: Outlet) -> Optional[int]:
        """Create new outlet"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO outlets (name, official_url, domain, detected_at, metadata)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    outlet.name,
                    outlet.official_url,
                    outlet.domain,
                    outlet.detected_at.isoformat() if outlet.detected_at else datetime.now().isoformat(),
                    json.dumps(outlet.metadata)
                ))
                logger.info(f"✅ Created outlet: {outlet.name} (ID: {cursor.lastrowid})")
                return cursor.lastrowid
                
        except sqlite3.IntegrityError:
            logger.warning(f"⚠️  Outlet '{outlet.name}' already exists")
            return None
        except Exception as e:
            logger.error(f"❌ Failed to create outlet: {e}")
            return None
    
    def get_outlet_by_name(self, name: str) -> Optional[Outlet]:
        """Get outlet by name"""
        try:
            with self.get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM outlets WHERE name = ?", (name,)
                ).fetchone()
                
                if row:
                    return Outlet(
                        id=row['id'],
                        name=row['name'],
                        official_url=row['official_url'],
                        domain=row['domain'],
                        detected_at=datetime.fromisoformat(row['detected_at']) if row['detected_at'] else None,
                        last_scraped=datetime.fromisoformat(row['last_scraped']) if row['last_scraped'] else None,
                        total_journalists=row['total_journalists'],
                        status=row['status'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    )
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting outlet by name: {e}")
            return None
    
    def get_outlet_by_id(self, outlet_id: int) -> Optional[Outlet]:
        """Get outlet by ID"""
        try:
            with self.get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM outlets WHERE id = ?", (outlet_id,)
                ).fetchone()
                
                if row:
                    return Outlet(
                        id=row['id'],
                        name=row['name'],
                        official_url=row['official_url'],
                        domain=row['domain'],
                        detected_at=datetime.fromisoformat(row['detected_at']) if row['detected_at'] else None,
                        last_scraped=datetime.fromisoformat(row['last_scraped']) if row['last_scraped'] else None,
                        total_journalists=row['total_journalists'],
                        status=row['status'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    )
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting outlet by ID: {e}")
            return None
    
    def get_all_outlets(self) -> List[Outlet]:
        """Get all outlets"""
        outlets = []
        try:
            with self.get_connection() as conn:
                rows = conn.execute(
                    "SELECT * FROM outlets ORDER BY name"
                ).fetchall()
                
                for row in rows:
                    outlets.append(Outlet(
                        id=row['id'],
                        name=row['name'],
                        official_url=row['official_url'],
                        domain=row['domain'],
                        detected_at=datetime.fromisoformat(row['detected_at']) if row['detected_at'] else None,
                        last_scraped=datetime.fromisoformat(row['last_scraped']) if row['last_scraped'] else None,
                        total_journalists=row['total_journalists'],
                        status=row['status'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    ))
            
        except Exception as e:
            logger.error(f"❌ Error getting all outlets: {e}")
        
        return outlets
    
    def update_outlet_scraped(self, outlet_id: int, journalist_count: int):
        """Update outlet last scraped time and journalist count"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    UPDATE outlets 
                    SET last_scraped = ?, total_journalists = ?
                    WHERE id = ?
                """, (datetime.now().isoformat(), journalist_count, outlet_id))
                
                logger.info(f"✅ Updated outlet {outlet_id}: {journalist_count} journalists")
                
        except Exception as e:
            logger.error(f"❌ Error updating outlet: {e}")
    
    # ==================== JOURNALIST OPERATIONS ====================
    
    def create_journalist(self, journalist: Journalist) -> Optional[int]:
        """Create new journalist"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO journalists (
                        name, outlet_id, beat, contact_email, contact_phone,
                        bio, profile_url, twitter_handle, linkedin_url,
                        first_seen, article_count, metadata
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    journalist.name,
                    journalist.outlet_id,
                    journalist.beat,
                    journalist.contact_email,
                    journalist.contact_phone,
                    journalist.bio,
                    journalist.profile_url,
                    journalist.twitter_handle,
                    journalist.linkedin_url,
                    journalist.first_seen.isoformat() if journalist.first_seen else datetime.now().isoformat(),
                    journalist.article_count,
                    json.dumps(journalist.metadata)
                ))
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"❌ Failed to create journalist: {e}")
            return None
    
    def get_journalists_by_outlet(self, outlet_id: int) -> List[Journalist]:
        """Get all journalists for an outlet"""
        journalists = []
        try:
            with self.get_connection() as conn:
                rows = conn.execute(
                    "SELECT * FROM journalists WHERE outlet_id = ? ORDER BY name", 
                    (outlet_id,)
                ).fetchall()
                
                for row in rows:
                    journalists.append(Journalist(
                        id=row['id'],
                        name=row['name'],
                        outlet_id=row['outlet_id'],
                        beat=row['beat'],
                        contact_email=row['contact_email'],
                        contact_phone=row['contact_phone'],
                        bio=row['bio'],
                        profile_url=row['profile_url'],
                        twitter_handle=row['twitter_handle'],
                        linkedin_url=row['linkedin_url'],
                        first_seen=datetime.fromisoformat(row['first_seen']) if row['first_seen'] else None,
                        last_updated=datetime.fromisoformat(row['last_updated']) if row['last_updated'] else None,
                        article_count=row['article_count'],
                        influence_score=row['influence_score'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    ))
            
        except Exception as e:
            logger.error(f"❌ Error getting journalists: {e}")
        
        return journalists
    
    def get_all_journalists(self) -> List[Journalist]:
        """Get all journalists"""
        journalists = []
        try:
            with self.get_connection() as conn:
                rows = conn.execute(
                    "SELECT * FROM journalists ORDER BY name"
                ).fetchall()
                
                for row in rows:
                    journalists.append(Journalist(
                        id=row['id'],
                        name=row['name'],
                        outlet_id=row['outlet_id'],
                        beat=row['beat'],
                        contact_email=row['contact_email'],
                        contact_phone=row['contact_phone'],
                        bio=row['bio'],
                        profile_url=row['profile_url'],
                        twitter_handle=row['twitter_handle'],
                        linkedin_url=row['linkedin_url'],
                        first_seen=datetime.fromisoformat(row['first_seen']) if row['first_seen'] else None,
                        last_updated=datetime.fromisoformat(row['last_updated']) if row['last_updated'] else None,
                        article_count=row['article_count'],
                        influence_score=row['influence_score'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    ))
            
        except Exception as e:
            logger.error(f"❌ Error getting all journalists: {e}")
        
        return journalists
    
    def update_influence_score(self, journalist_id: int, score: float):
        """Update journalist influence score"""
        try:
            with self.get_connection() as conn:
                conn.execute(
                    "UPDATE journalists SET influence_score = ? WHERE id = ?",
                    (score, journalist_id)
                )
                logger.info(f"✅ Updated influence score for journalist {journalist_id}: {score}")
                
        except Exception as e:
            logger.error(f"❌ Error updating influence score: {e}")
    
    # ==================== SCRAPING JOB OPERATIONS ====================
    
    def create_scraping_job(self, outlet_name: str) -> int:
        """Create new scraping job"""
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO scraping_jobs (outlet_name, status, started_at)
                    VALUES (?, 'running', ?)
                """, (outlet_name, datetime.now().isoformat()))
                
                logger.info(f"✅ Created scraping job {cursor.lastrowid} for '{outlet_name}'")
                return cursor.lastrowid
                
        except Exception as e:
            logger.error(f"❌ Error creating scraping job: {e}")
            return 0
    
    def update_scraping_job(self, job_id: int, status: str, profiles_found: int = 0, error: str = None):
        """Update scraping job status"""
        try:
            with self.get_connection() as conn:
                conn.execute("""
                    UPDATE scraping_jobs
                    SET status = ?, profiles_found = ?, completed_at = ?, error_message = ?
                    WHERE id = ?
                """, (status, profiles_found, datetime.now().isoformat(), error, job_id))
                
                logger.info(f"✅ Updated job {job_id}: status={status}, profiles={profiles_found}")
                
        except Exception as e:
            logger.error(f"❌ Error updating scraping job: {e}")
    
    def get_recent_jobs(self, limit: int = 10) -> List[ScrapingJob]:
        """Get recent scraping jobs"""
        jobs = []
        try:
            with self.get_connection() as conn:
                rows = conn.execute("""
                    SELECT * FROM scraping_jobs 
                    ORDER BY started_at DESC 
                    LIMIT ?
                """, (limit,)).fetchall()
                
                for row in rows:
                    jobs.append(ScrapingJob(
                        id=row['id'],
                        outlet_name=row['outlet_name'],
                        status=row['status'],
                        profiles_found=row['profiles_found'],
                        started_at=datetime.fromisoformat(row['started_at']) if row['started_at'] else None,
                        completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                        error_message=row['error_message'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    ))
            
        except Exception as e:
            logger.error(f"❌ Error getting recent jobs: {e}")
        
        return jobs
    
    def get_job_by_id(self, job_id: int) -> Optional[ScrapingJob]:
        """Get scraping job by ID"""
        try:
            with self.get_connection() as conn:
                row = conn.execute(
                    "SELECT * FROM scraping_jobs WHERE id = ?", (job_id,)
                ).fetchone()
                
                if row:
                    return ScrapingJob(
                        id=row['id'],
                        outlet_name=row['outlet_name'],
                        status=row['status'],
                        profiles_found=row['profiles_found'],
                        started_at=datetime.fromisoformat(row['started_at']) if row['started_at'] else None,
                        completed_at=datetime.fromisoformat(row['completed_at']) if row['completed_at'] else None,
                        error_message=row['error_message'],
                        metadata=json.loads(row['metadata']) if row['metadata'] else {}
                    )
            return None
            
        except Exception as e:
            logger.error(f"❌ Error getting job by ID: {e}")
            return None
    
    # ==================== UTILITY METHODS ====================
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get database statistics"""
        stats = {
            'total_outlets': 0,
            'total_journalists': 0,
            'total_jobs': 0,
            'completed_jobs': 0,
            'failed_jobs': 0
        }
        
        try:
            with self.get_connection() as conn:
                # Count outlets
                stats['total_outlets'] = conn.execute(
                    "SELECT COUNT(*) as count FROM outlets"
                ).fetchone()['count']
                
                # Count journalists
                stats['total_journalists'] = conn.execute(
                    "SELECT COUNT(*) as count FROM journalists"
                ).fetchone()['count']
                
                # Count jobs
                stats['total_jobs'] = conn.execute(
                    "SELECT COUNT(*) as count FROM scraping_jobs"
                ).fetchone()['count']
                
                # Count completed jobs
                stats['completed_jobs'] = conn.execute(
                    "SELECT COUNT(*) as count FROM scraping_jobs WHERE status = 'completed'"
                ).fetchone()['count']
                
                # Count failed jobs
                stats['failed_jobs'] = conn.execute(
                    "SELECT COUNT(*) as count FROM scraping_jobs WHERE status = 'failed'"
                ).fetchone()['count']
            
        except Exception as e:
            logger.error(f"❌ Error getting statistics: {e}")
        
        return stats
    
    def clear_all_data(self):
        """Clear all data from database (for testing)"""
        try:
            with self.get_connection() as conn:
                conn.execute("DELETE FROM journalist_topics")
                conn.execute("DELETE FROM cross_outlet_matches")
                conn.execute("DELETE FROM articles")
                conn.execute("DELETE FROM journalists")
                conn.execute("DELETE FROM outlets")
                conn.execute("DELETE FROM topics")
                conn.execute("DELETE FROM scraping_jobs")
                
            logger.info("✅ All data cleared from database")
            
        except Exception as e:
            logger.error(f"❌ Error clearing data: {e}")


# Global database instance
db_manager = DatabaseManager()


def init_db():
    """Initialize database (called from Flask app factory)"""
    return db_manager.init_database()
