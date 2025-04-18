import os

API_KEY = os.environ.get('API_KEY')
DEBUG = os.environ.get('DEBUG', '').lower() in ("1", "true", "yes", "on")
