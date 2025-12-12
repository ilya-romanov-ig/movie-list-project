from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List

model_cfg = ConfigDict(from_attributes=True)

class ActorBase(BaseModel):
    model_config = model_cfg

    id: str
    name: str


class ActorListItem(ActorBase):
    pass


class ActorFilmographyItem(BaseModel):
    model_config = model_cfg

    id: int            # film id
    title: str
    release_year: int
    role: Optional[str] = None
    watched_count: Optional[int] = None


class ActorDetail(ActorBase):
    birth_year: Optional[int] = None
    death_year: Optional[int] = None
    favorites_count: Optional[int] = None
    filmography: list[ActorFilmographyItem] = Field(default_factory=list)
