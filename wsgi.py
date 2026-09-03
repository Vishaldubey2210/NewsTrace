"""
NewsTrace WSGI Entry Point
Used by production application servers (Gunicorn, uWSGI, Waitress).
"""

import os
from config import get_config
from app import create_app

env = os.getenv('FLASK_ENV', 'production')
app = create_app(get_config(env))

if __name__ == '__main__':
    app.run()
