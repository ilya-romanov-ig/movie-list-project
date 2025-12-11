# app/routers/search.py

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.search import (
    search_films,
    search_actors,
    search_users
)

router = APIRouter(prefix="/search", tags=["Search"])


@router.get("/")
async def global_search(
    q: str = Query(..., description="Search query"),
    db: AsyncSession = Depends(get_db),
):
    films = await search_films(db, q)
    actors = await search_actors(db, q)
    users = await search_users(db, q)

    return {
        "query": q,
        "results": {
            "films": [{"id": f.film_id, "title": f.title} for f in films],
            "actors": [{"id": a.actor_id, "name": a.name} for a in actors],
            "users": [{"id": u.user_id, "username": u.username} for u in users]
        }
    }
