# app/routers/favorites.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.favorites import (
    add_favorite_film,
    remove_favorite_film,
    get_favorite_films,
    is_film_favorite,
    add_favorite_actor,
    remove_favorite_actor,
    get_favorite_actors,
    is_actor_favorite,
)

router = APIRouter(prefix="/favorites", tags=["Favorites"])


# ---------------------------------------------------------
# FAVORITE FILMS
# ---------------------------------------------------------

@router.post("/films/{film_id}")
async def add_favorite_film_route(
    film_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    await add_favorite_film(db, user_id=user_id, film_id=film_id)
    return {"status": "added", "film_id": film_id}


@router.delete("/films/{film_id}")
async def remove_favorite_film_route(
    film_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    ok = await remove_favorite_film(db, user_id=user_id, film_id=film_id)
    if not ok:
        raise HTTPException(404, "Not in favorites")
    return {"status": "removed", "film_id": film_id}


@router.get("/films")
async def list_favorite_films(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    films = await get_favorite_films(db, user_id)
    return {
        "count": len(films),
        "items": [
            {"film_id": f.film_id, "title": f.title}
            for f in films
        ]
    }


# ---------------------------------------------------------
# FAVORITE ACTORS
# ---------------------------------------------------------

@router.post("/actors/{actor_id}")
async def add_favorite_actor_route(
    actor_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    await add_favorite_actor(db, user_id=user_id, actor_id=actor_id)
    return {"status": "added", "actor_id": actor_id}


@router.delete("/actors/{actor_id}")
async def remove_favorite_actor_route(
    actor_id: int,
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    ok = await remove_favorite_actor(db, user_id=user_id, actor_id=actor_id)
    if not ok:
        raise HTTPException(404, "Not in favorites")
    return {"status": "removed", "actor_id": actor_id}


@router.get("/actors")
async def list_favorite_actors(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    actors = await get_favorite_actors(db, user_id)
    return {
        "count": len(actors),
        "items": [
            {"actor_id": a.actor_id, "name": a.name}
            for a in actors
        ]
    }
