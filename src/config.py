import os

from models.app import AppContext
from pathlib import Path

# src directory
BASE_DIR = Path(__file__).resolve().parent
# Project root directory (one level up from src/)
ROOT_DIR = BASE_DIR.parent

TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
POSTERS_DIR = ROOT_DIR / 'posters'  # Use root-level posters
THEMES_DIR = ROOT_DIR / 'themes'  # Use root-level themes
FONTS_DIR = ROOT_DIR / 'fonts'  # Use root-level fonts

# Initialize the context object
app_context = AppContext(
    name=os.environ.get('APP_NAME', "map-to-poster"),
    mode=os.environ.get('APP_MODE', "dev")
)