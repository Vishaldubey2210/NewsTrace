"""
NewsTrace Flask Application Factory - COMPLETE INTEGRATED VERSION
Combines all features with proper initialization
"""

from flask import Flask
try:
    from flask_cors import CORS
except ImportError:
    class CORS:
        def __init__(self, *args, **kwargs): pass
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os


def create_app(config_object=None):
    """
    Flask application factory with complete feature integration
    
    Args:
        config_object: Configuration object (from config.py)
    
    Returns:
        Configured Flask application instance
    """
    # Create Flask app
    app = Flask(
        __name__,
        template_folder='../frontend/templates',
        static_folder='../frontend/static'
    )
    
    # Load configuration
    if config_object:
        app.config.from_object(config_object)
    else:
        from config import get_config
        config = get_config()
        app.config.from_object(config)
    
    # Setup logging first (critical for debugging)
    setup_logging(app)
    app.logger.info("=" * 60)
    app.logger.info("NewsTrace Application Initialization")
    app.logger.info("=" * 60)
    
    # Enable CORS for API endpoints
    CORS(app, resources={
        r"/api/*": {
            "origins": "*",
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })
    app.logger.info("[OK] CORS enabled for API endpoints")
    
    # Initialize database
    with app.app_context():
        try:
            from app.database.sqlite_db import init_db
            init_db()
            app.logger.info("[OK] Database initialized successfully")
        except Exception as e:
            app.logger.error(f"[ERROR] Database initialization failed: {e}")
            raise
    
    # Initialize NLP modules
    init_nlp_modules(app)
    
    # Initialize analytics modules
    init_analytics_modules(app)
    
    # Initialize graph builder
    init_graph_modules(app)
    
    # Register routes
    try:
        from app.routes import register_routes
        register_routes(app)
        app.logger.info("[OK] Routes registered successfully")
    except Exception as e:
        app.logger.error(f"[ERROR] Route registration failed: {e}")
        raise
    
    # Log final startup info
    app.logger.info("=" * 60)
    app.logger.info(f"Environment: {app.config.get('FLASK_ENV', 'development')}")
    app.logger.info(f"Debug Mode: {app.config.get('DEBUG', False)}")
    app.logger.info(f"Database: {app.config.get('DATABASE_PATH')}")
    app.logger.info("[SUCCESS] NewsTrace application started successfully")
    app.logger.info("=" * 60)
    
    return app


def setup_logging(app):
    """
    Configure comprehensive logging system
    
    Args:
        app: Flask application instance
    """
    # Get log configuration from app config
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO'))
    log_file = app.config.get('LOG_FILE')
    log_format = app.config.get('LOG_FORMAT', 
                                '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Create formatter
    formatter = logging.Formatter(log_format, datefmt='%Y-%m-%d %H:%M:%S')
    
    # Remove existing handlers
    app.logger.handlers = []
    
    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    app.logger.addHandler(console_handler)
    
    # File handler (rotating) for production
    if log_file:
        try:
            # Ensure log directory exists
            log_dir = Path(log_file).parent
            log_dir.mkdir(parents=True, exist_ok=True)
            
            file_handler = RotatingFileHandler(
                log_file,
                maxBytes=app.config.get('LOG_MAX_BYTES', 10 * 1024 * 1024),  # 10MB
                backupCount=app.config.get('LOG_BACKUP_COUNT', 5)
            )
            file_handler.setLevel(log_level)
            file_handler.setFormatter(formatter)
            app.logger.addHandler(file_handler)
        except Exception as e:
            print(f"[WARNING] Could not setup file logging: {e}")
    
    # Set app logger level
    app.logger.setLevel(log_level)
    
    # Prevent propagation to root logger
    app.logger.propagate = False
    
    app.logger.info("[OK] Logging configured successfully")


def init_nlp_modules(app):
    """
    Initialize Natural Language Processing modules
    
    Args:
        app: Flask application instance
    """
    app.logger.info("[INIT] Loading NLP modules...")
    
    try:
        # Import NLP modules
        from app.nlp.entity_extractor import entity_extractor
        from app.nlp.sentiment_analyzer import sentiment_analyzer
        from app.nlp.keyword_extractor import keyword_extractor
        from app.nlp.topic_modeler import topic_modeler
        
        # Store in app context
        app.nlp = {
            'entity_extractor': entity_extractor,
            'sentiment_analyzer': sentiment_analyzer,
            'keyword_extractor': keyword_extractor,
            'topic_modeler': topic_modeler
        }
        
        app.logger.info("[OK] NLP modules loaded:")
        app.logger.info("  - Entity Extractor (spaCy)")
        app.logger.info("  - Sentiment Analyzer (TextBlob)")
        app.logger.info("  - Keyword Extractor (TF-IDF)")
        app.logger.info("  - Topic Modeler (LDA)")
        
    except ImportError as e:
        app.logger.warning(f"[WARN] Some NLP modules unavailable: {e}")
        app.logger.warning("  Install missing dependencies: pip install textblob scikit-learn")
        app.nlp = None
    except Exception as e:
        app.logger.error(f"[ERROR] NLP initialization failed: {e}")
        app.nlp = None


def init_analytics_modules(app):
    """
    Initialize Analytics and Intelligence modules
    
    Args:
        app: Flask application instance
    """
    app.logger.info("[INIT] Loading Analytics modules...")
    
    try:
        # Import analytics modules
        from app.analytics.influence_score import influence_calculator
        from app.analytics.cross_outlet_tracker import cross_outlet_tracker
        from app.analytics.community_detector import community_detector
        from app.analytics.bias_detector import bias_detector
        
        # Store in app context
        app.analytics = {
            'influence_calculator': influence_calculator,
            'cross_outlet_tracker': cross_outlet_tracker,
            'community_detector': community_detector,
            'bias_detector': bias_detector
        }
        
        app.logger.info("[OK] Analytics modules loaded:")
        app.logger.info("  - Influence Score Calculator")
        app.logger.info("  - Cross-Outlet Tracker (Fuzzy Matching)")
        app.logger.info("  - Community Detector (NetworkX)")
        app.logger.info("  - Bias Detector")
        
    except ImportError as e:
        app.logger.warning(f"[WARN] Some Analytics modules unavailable: {e}")
        app.logger.warning("  Install: pip install fuzzywuzzy python-louvain")
        app.analytics = None
    except Exception as e:
        app.logger.error(f"[ERROR] Analytics initialization failed: {e}")
        app.analytics = None


def init_graph_modules(app):
    """
    Initialize Graph and Network modules
    
    Args:
        app: Flask application instance
    """
    app.logger.info("[INIT] Loading Graph modules...")
    
    try:
        # Import graph modules
        from app.database.graph_builder import graph_builder
        
        # Store in app context
        app.graph_builder = graph_builder
        
        app.logger.info("[OK] Graph modules loaded:")
        app.logger.info("  - NetworkX Graph Builder")
        app.logger.info("  - Vis.js Export Support")
        
    except ImportError as e:
        app.logger.warning(f"[WARN] Graph modules unavailable: {e}")
        app.logger.warning("  Install: pip install networkx")
        app.graph_builder = None
    except Exception as e:
        app.logger.error(f"[ERROR] Graph initialization failed: {e}")
        app.graph_builder = None


# Module-level exports
__all__ = ['create_app']
