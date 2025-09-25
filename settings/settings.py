# Plain settings module (Django-style)
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_NAME = "Metal Workers API"
DEBUG = False


# New template/static locations
TEMPLATES_DIR = str(PROJECT_ROOT / "templates")
STATIC_DIR = str(PROJECT_ROOT / "static")

# Database settings
DATABASE_URL = "sqlite:///./metalworkers.db"
