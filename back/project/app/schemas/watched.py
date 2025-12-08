from pydantic import BaseModel, Field, ConfigDict
from app.schemas.film import FilmListItem
from typing import Optional

model_cfg = ConfigDict(from_attributes=True)

class WatchedAdd(BaseModel):
    film_id: int


class WatchedFilmOut(BaseModel):
    model_config = model_cfg

    film: FilmListItem
    watched_at: str
