from pydantic import BaseModel


class CreatePoster(BaseModel):
    city: str
    country: str
    theme: str
    distance: int