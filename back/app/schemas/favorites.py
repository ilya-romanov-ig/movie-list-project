from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from app.schemas.film import FilmListItem
from app.schemas.actor import ActorListItem

model_cfg = ConfigDict(from_attributes=True)

class FavoriteFilmOut(BaseModel):
    model_config = model_cfg

    film: FilmListItem
    added_at: str


class FavoriteActorOut(BaseModel):
    model_config = model_cfg

    actor: ActorListItem
    added_at: str


class FavoriteFilmAdd(BaseModel):
    film_id: int


class FavoriteActorAdd(BaseModel):
    actor_id: int
