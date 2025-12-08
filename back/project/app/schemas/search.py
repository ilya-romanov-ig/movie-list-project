from pydantic import BaseModel
from app.schemas.film import FilmListItem
from app.schemas.actor import ActorListItem
from app.schemas.user import UserListItem

class SearchResponse(BaseModel):
    films: list[FilmListItem] = []
    actors: list[ActorListItem] = []
    users: list[UserListItem] = []
