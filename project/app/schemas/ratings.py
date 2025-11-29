from pydantic import BaseModel, ConfigDict
from typing import Optional
from app.schemas.film import FilmListItem

model_cfg = ConfigDict(from_attributes=True)

class RatingAdd(BaseModel):
    film_id: int
    rating: int


class RatingUpdate(BaseModel):
    rating: int


class RatingOut(BaseModel):
    model_config = model_cfg

    user_id: int
    film_id: int
    rating: int
    rated_at: str


class UserRatedFilmOut(BaseModel):
    model_config = model_cfg

    film: FilmListItem
    rating: Optional[int] = None
    rated_at: Optional[str] = None
