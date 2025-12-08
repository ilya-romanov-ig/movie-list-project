from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional

model_cfg = ConfigDict(from_attributes=True)

class FilmBase(BaseModel):
    model_config = model_cfg

    id: int
    title: str
    release_year: int
    runtime: Optional[int] = None
    poster_url: Optional[str] = None


class FilmListItem(BaseModel):
    model_config = model_cfg

    id: int
    title: str
    release_year: int
    rating: Optional[float] = None


class FilmDetail(FilmBase):
    description: Optional[str] = None
    genres: list[str] = Field(default_factory=list)
    actors: list[str] = Field(default_factory=list)
    avg_rating: Optional[float] = None
    n_ratings: Optional[int] = None
    watched_count: Optional[int] = None
    favorites_count: Optional[int] = None


class FilmCreate(BaseModel):
    model_config = model_cfg

    title: str
    release_year: int
    runtime: Optional[int] = None
    description: Optional[str] = None
    poster_url: Optional[str] = None
