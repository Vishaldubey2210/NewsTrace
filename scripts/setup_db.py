# Placeholder file
"""
NewsTrace Database Setup Script
Initialize database with schema
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database.sqlite_db import db_manager
from config import Config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    """Setup database"""
    print("=" * 60)
    print("📦 NewsTrace Database Setup")
    print("=" * 60)
    print()
    
    print(f"Database path: {Config.DATABASE_PATH}")
    print()
    
    # Initialize database
    print("🔨 Creating database schema...")
    success = db_manager.init_database()
    
    if success:
        print("✅ Database setup completed successfully!")
        print()
        print("Next steps:")
        print("1. Run the Flask application: python run.py")
        print("2. Open browser: http://localhost:5000")
    else:
        print("❌ Database setup failed!")
        sys.exit(1)


if __name__ == '__main__':
    main()
