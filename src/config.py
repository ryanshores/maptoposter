import os

from src.models.app import AppContext

# Initialize the context object
app_context = AppContext(
    name=os.environ.get('APP_NAME', "map-to-poster"),
    mode=os.environ.get('APP_MODE', "dev")
)