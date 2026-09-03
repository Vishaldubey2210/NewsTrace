"""
NewsTrace Application Runner
Main entry point for the Flask application
"""

import os
import sys
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.resolve()
sys.path.insert(0, str(PROJECT_ROOT))

# Import from root level
from config import get_config
from app import create_app

# Expose WSGI application callable for production servers (Gunicorn, Waitress, uWSGI)
env_name = os.getenv('FLASK_ENV', 'production')
app = create_app(get_config(env_name))


def main():
    """Main application entry point"""
    
    # Get configuration
    env = os.getenv('FLASK_ENV', 'development')
    
    try:
        config = get_config(env)
    except Exception as e:
        print(f"[ERROR] Failed to load configuration: {e}")
        sys.exit(1)
    
    # Create Flask app
    try:
        flask_app = create_app(config)
    except Exception as e:
        print(f"[ERROR] Failed to create Flask app: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Get host and port from environment or use defaults
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    # Welcome banner
    print("\n" + "=" * 70)
    print("🚀 NewsTrace - Autonomous Media Intelligence System")
    print("=" * 70)
    print(f"📌 Environment     : {env.upper()}")
    print(f"🐛 Debug Mode      : {config.DEBUG}")
    print(f"💾 Database        : {config.DATABASE_PATH}")
    print(f"📁 Export Path     : {config.EXPORT_PATH}")
    print(f"📊 Min Profiles    : {config.MIN_PROFILES_REQUIRED}")
    print(f"🌐 Running on      : http://{host}:{port}")
    print(f"📖 API Health      : http://{host}:{port}/api/health")
    print("=" * 70)
    print("💡 Press CTRL+C to stop the server")
    print("=" * 70 + "\n")
    
    # Run the application
    try:
        flask_app.run(
            host=host,
            port=port,
            debug=config.DEBUG,
            threaded=True,
            use_reloader=config.DEBUG  # Auto-reload in development
        )
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("👋 NewsTrace server stopped")
        print("=" * 70)
    except Exception as e:
        print("\n" + "=" * 70)
        print(f"❌ Error starting server: {e}")
        print("=" * 70)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
