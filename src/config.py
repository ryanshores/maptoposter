import os

from src.models.app import AppContext
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # Gets the absolute path to the project root
TEMPLATES_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
POSTERS_DIR = BASE_DIR / 'posters'
THEMES_DIR = BASE_DIR / 'themes'
FONTS_DIR = BASE_DIR / 'fonts'

# Initialize the context object
app_context = AppContext(
    name=os.environ.get('APP_NAME', "map-to-poster"),
    mode=os.environ.get('APP_MODE', "dev")
)