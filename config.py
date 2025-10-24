"""
NewsTrace Configuration Module
Manages all application settings and configurations
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory - PROJECT ROOT
BASE_DIR = Path(__file__).parent.resolve()  # ✅ Points to NewsTrace_full/
DATA_DIR = BASE_DIR / 'data'
LOG_DIR = BASE_DIR / 'logs'

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR.mkdir(exist_ok=True, parents=True)
(DATA_DIR / 'database').mkdir(exist_ok=True, parents=True)
(DATA_DIR / 'cache').mkdir(exist_ok=True, parents=True)
(DATA_DIR / 'exports').mkdir(exist_ok=True, parents=True)
(DATA_DIR / 'graphs').mkdir(exist_ok=True, parents=True)

print(f"[CONFIG] BASE_DIR: {BASE_DIR}")
print(f"[CONFIG] DATA_DIR: {DATA_DIR}")
print(f"[CONFIG] LOG_DIR: {LOG_DIR}")
print(f"[CONFIG] EXPORT_PATH: {DATA_DIR / 'exports'}")


class Config:
    """Base configuration class"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    FLASK_APP = os.getenv('FLASK_APP', 'run.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = FLASK_ENV == 'development'
    
    # Database Configuration
    DATABASE_PATH = os.getenv('DATABASE_PATH', str(DATA_DIR / 'database' / 'newstrace.db'))
    DATABASE_URI = f'sqlite:///{DATABASE_PATH}'
    
    # Scraping Configuration
    USER_AGENT_ROTATION = os.getenv('USER_AGENT_ROTATION', 'True').lower() == 'true'
    RESPECT_ROBOTS_TXT = os.getenv('RESPECT_ROBOTS_TXT', 'False').lower() == 'true'
    SCRAPING_DELAY = int(os.getenv('SCRAPING_DELAY', 5))
    MAX_RETRIES = int(os.getenv('MAX_RETRIES', 3))
    REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 60))
    
    # Search API Configuration
    GOOGLE_SEARCH_ENABLED = os.getenv('GOOGLE_SEARCH_ENABLED', 'False').lower() == 'true'
    DUCKDUCKGO_SEARCH_ENABLED = os.getenv('DUCKDUCKGO_SEARCH_ENABLED', 'True').lower() == 'true'
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', str(LOG_DIR / 'newstrace.log'))
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10 MB
    LOG_BACKUP_COUNT = 5
    
    # Application Settings
    MAX_PROFILES_PER_OUTLET = int(os.getenv('MAX_PROFILES_PER_OUTLET', 50))
    MIN_PROFILES_REQUIRED = int(os.getenv('MIN_PROFILES_REQUIRED', 30))
    ENABLE_CACHING = os.getenv('ENABLE_CACHING', 'True').lower() == 'true'
    CACHE_DURATION = int(os.getenv('CACHE_DURATION', 3600))  # 1 hour
    CACHE_DIR = str(DATA_DIR / 'cache')
    
    # NLP Settings
    SPACY_MODEL = os.getenv('SPACY_MODEL', 'en_core_web_sm')
    ENABLE_TOPIC_MODELING = os.getenv('ENABLE_TOPIC_MODELING', 'True').lower() == 'true'
    ENABLE_SENTIMENT_ANALYSIS = os.getenv('ENABLE_SENTIMENT_ANALYSIS', 'False').lower() == 'true'
    MIN_TOPIC_CONFIDENCE = 0.3
    
    # Export Settings
    DEFAULT_EXPORT_FORMAT = os.getenv('DEFAULT_EXPORT_FORMAT', 'csv')
    EXPORT_PATH = str(DATA_DIR / 'exports')
    GRAPH_EXPORT_PATH = str(DATA_DIR / 'graphs')
    
    # Agent Settings
    AGENT_TIMEOUT = int(os.getenv('AGENT_TIMEOUT', 60))
    MAX_AGENT_RETRIES = int(os.getenv('MAX_AGENT_RETRIES', 3))
    
    # Graph Settings
    GRAPH_MIN_CONNECTIONS = int(os.getenv('GRAPH_MIN_CONNECTIONS', 1))
    GRAPH_LAYOUT = os.getenv('GRAPH_LAYOUT', 'force_directed')
    ENABLE_GRAPH_CACHING = os.getenv('ENABLE_GRAPH_CACHING', 'True').lower() == 'true'
    
    # Analytics Settings
    INFLUENCE_SCORE_WEIGHTS = {
        'article_count': 0.4,
        'topic_diversity': 0.3,
        'recency': 0.2,
        'cross_outlet': 0.1
    }
    
    # Frontend Settings
    STATIC_FOLDER = 'frontend/static'
    TEMPLATE_FOLDER = 'frontend/templates'
    ITEMS_PER_PAGE = int(os.getenv('ITEMS_PER_PAGE', 20))
    
    # Real-time Scraping Settings
    PLAYWRIGHT_HEADLESS = os.getenv('PLAYWRIGHT_HEADLESS', 'True').lower() == 'true'
    PLAYWRIGHT_TIMEOUT = int(os.getenv('PLAYWRIGHT_TIMEOUT', 30000))  # milliseconds
    BEAUTIFULSOUP_PARSER = os.getenv('BEAUTIFULSOUP_PARSER', 'lxml')
    
    # Fallback Profile Generation
    ENABLE_FALLBACK_PROFILES = os.getenv('ENABLE_FALLBACK_PROFILES', 'True').lower() == 'true'
    FALLBACK_PROFILE_COUNT = int(os.getenv('FALLBACK_PROFILE_COUNT', 30))


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False
    SCRAPING_DELAY = 2


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    SCRAPING_DELAY = 5
    REQUEST_TIMEOUT = 60
    RESPECT_ROBOTS_TXT = True


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ':memory:'
    ENABLE_CACHING = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    return config.get(env, config['default'])


def validate_config():
    """Validate critical configuration settings"""
    issues = []
    
    # Check database directory
    db_dir = Path(Config.DATABASE_PATH).parent
    if not db_dir.exists():
        try:
            db_dir.mkdir(parents=True, exist_ok=True)
            print(f"[CONFIG] Created database directory: {db_dir}")
        except Exception as e:
            issues.append(f"Cannot create database directory {db_dir}: {e}")
    
    # Check export directory
    export_dir = Path(Config.EXPORT_PATH)
    if not export_dir.exists():
        try:
            export_dir.mkdir(parents=True, exist_ok=True)
            print(f"[CONFIG] Created export directory: {export_dir}")
        except Exception as e:
            issues.append(f"Cannot create export directory {export_dir}: {e}")
    
    # Check log directory
    log_dir = Path(Config.LOG_FILE).parent
    if not log_dir.exists():
        try:
            log_dir.mkdir(parents=True, exist_ok=True)
            print(f"[CONFIG] Created log directory: {log_dir}")
        except Exception as e:
            issues.append(f"Cannot create log directory {log_dir}: {e}")
    
    if issues:
        print("[WARNING] Configuration issues detected:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("[CONFIG] ✅ All directories validated successfully")
        print(f"[CONFIG] ✅ Database: {Config.DATABASE_PATH}")
        print(f"[CONFIG] ✅ Exports: {Config.EXPORT_PATH}")
        print(f"[CONFIG] ✅ Logs: {Config.LOG_FILE}")
        return True


# Run validation
validate_config()
