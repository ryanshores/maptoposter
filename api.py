import logging
import os
import typing
from pathlib import Path

import uvicorn
from fastapi import Request, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.routing import APIRoute as Route
from fastapi.routing import Mount
from create_map_poster import create_poster, POSTERS_DIR
from models.api import ApiContext
from config import app_context

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
        'api': api_context
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
    return templates.TemplateResponse(
        "generate.html",
        {
            "request": request,
            "title": f"{app_context.name} - Generate Poster"
        }
    )

async def create_poster_view(request: Request):
    """Generates a new poster."""
    city, country = request.query_params["city"], request.query_params["country"]
    theme_name = request.query_params.get("theme", "default")
    distance = request.query_params.get("distance", 6000)
    output_file = create_poster(city, country, theme_name, distance)
    return {"file": output_file}


routes = [
    Route("/", endpoint=home, methods=["GET"]),
    Route("/posters", endpoint=get_posters, methods=["GET"]),
    Route("/generate", endpoint=generate, methods=["GET"]),
    Route("/create_poster", endpoint=create_poster_view, methods=["GET"]),
    Mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static"),
    Mount("/s/posters", StaticFiles(directory=str(POSTERS_DIR)), name="posters")
]

app = FastAPI(
    title=f'{app_context.name} ({app_context.mode})',
    routes=routes
)

if __name__ == "__main__":
    uvicorn.run("api:app", host=HOST, port=PORT, reload=True)
