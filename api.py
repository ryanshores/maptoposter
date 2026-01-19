import logging
import os
import threading
import typing
from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import Request, FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute as Route
from fastapi.routing import Mount
from create_map_poster import create_poster, POSTERS_DIR
from models.api import ApiContext
from config import app_context
from models.create_poster import CreatePoster

# Configuration
BASE_DIR = Path(__file__).resolve().parent  # Gets the absolute path to the project root
HOST = "0.0.0.0"
PORT = 8000
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
POSTERS_DIR = BASE_DIR / POSTERS_DIR

api_context = ApiContext(
    api_key=os.environ.get('API_KEY'),
    api_version="v1",
    base_url=os.environ.get('BASE_URL', 'http://localhost:8000').rstrip('/'),
)._asdict()

def get_app_context(request: Request) -> typing.Dict[str, typing.Any]:
    return {
        'app': app_context,
        'api': api_context,
    }

templates = Jinja2Templates(directory=str(TEMPLATES_DIR), context_processors=[get_app_context])

logger = logging.getLogger("uvicorn.error")


async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": f"{app_context.name} ({app_context.mode}) - Home"
        }
    )


async def get_posters(request: Request):
    """Lists generated posters."""
    image_extensions = (".png", ".jpg", ".jpeg")
    files = [f for f in os.listdir(POSTERS_DIR) if f.endswith(image_extensions)]

    logger.info(f"Found {len(files)} generated poster(s).")

    # Using a template for better readability and maintenance
    return templates.TemplateResponse(
        "posters.html",
        {
            "request": request,
            "title": f"{app_context.name} - Posters",
            "files": files,
        }
    )

async def generate(request: Request):
    themes = os.listdir(os.path.join(BASE_DIR, "themes"))
    return templates.TemplateResponse(
        "generate.html",
        {
            "request": request,
            "title": f"{app_context.name} - Generate Poster",
            "themes": themes,
        }
    )

async def create_poster_view(data: Annotated[CreatePoster, Form()]):
    """Generates a new poster."""
    try:
        # run in a different thread so a server restart doesn't block
        thread = threading.Thread(target=create_poster, args=(data.city, data.country, data.theme, data.distance))
        thread.start()
        return {"status": "OK"}
    except Exception as e:
        return {"status": str(e)}


routes = [
    Route("/", endpoint=home, methods=["GET"]),
    Route("/posters", endpoint=get_posters, methods=["GET"]),
    Route("/generate", endpoint=generate, methods=["GET"]),
    Route("/create_poster", endpoint=create_poster_view, methods=["POST"]),
    Mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static"),
    Mount("/s/posters", StaticFiles(directory=str(POSTERS_DIR)), name="posters")
]

app = FastAPI(
    title=f'{app_context.name} ({app_context.mode})',
    routes=routes
)

if __name__ == "__main__":
    uvicorn.run("api:app", host=HOST, port=PORT, reload=True)
