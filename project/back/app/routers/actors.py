# app/routers/actors.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.actors import (
    list_actors,
    get_actor_by_id,
    create_actor,
    update_actor,
    delete_actor,
    get_films_of_actor
)

router = APIRouter(prefix="/actors", tags=["Actors"])


# --------------------------
# GET /actors
# --------------------------
@router.get("")
async def get_all_actors(
    db: AsyncSession = Depends(get_db),
    limit: int = 20,
    offset: int = 0,
    name: str | None = None,
):
    actors = await list_actors(db, limit=limit, offset=offset, name_query=name)
    return {
        "count": len(actors),
        "items": [
            {"actor_id": a.actor_id, "name": a.name}
            for a in actors
        ]
    }


# --------------------------
# GET /actors/{actor_id}
# --------------------------
@router.get("/{actor_id}")
async def get_actor(actor_id: str, db: AsyncSession = Depends(get_db)):
    actor = await get_actor_by_id(db, actor_id)
    if not actor:
        raise HTTPException(404, "Actor not found")

    return {
        "actor_id": actor.actor_id,
        "name": actor.name,
        "birth_year": actor.birth_year,
        "bio": actor.bio,
        "photo_url": actor.photo_url,
    }


# --------------------------
# GET /actors/{actor_id}/films
# --------------------------
@router.get("/{actor_id}/films")
async def get_actor_films(actor_id: str, db: AsyncSession = Depends(get_db)):
    films = await get_films_of_actor(db, actor_id)

    return {
        "count": len(films),
        "items": [
            {"film_id": f.film_id, "title": f.title}
            for f in films
        ]
    }


# --------------------------
# POST /actors
# --------------------------
@router.post("")
async def create_new_actor(
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    if not data.get("name"):
        raise HTTPException(400, "Field 'name' is required")

    actor = await create_actor(
        db,
        name=data.get("name"),
        bio=data.get("bio"),
        birth_year=data.get("birth_year"),
        photo_url=data.get("photo_url"),
    )

    return {"status": "created", "actor_id": actor.actor_id}


# --------------------------
# PATCH /actors/{actor_id}
# --------------------------
@router.patch("/{actor_id}")
async def edit_actor(actor_id: str, data: dict, db: AsyncSession = Depends(get_db)):
    actor = await update_actor(
        db,
        actor_id,
        name=data.get("name"),
        bio=data.get("bio"),
        birth_year=data.get("birth_year"),
        photo_url=data.get("photo_url"),
    )

    if not actor:
        raise HTTPException(404, "Actor not found")

    return {"status": "updated"}


# --------------------------
# DELETE /actors/{actor_id}
# --------------------------
@router.delete("/{actor_id}")
async def remove_actor(actor_id: str, db: AsyncSession = Depends(get_db)):
    ok = await delete_actor(db, actor_id)
    if not ok:
        raise HTTPException(404, "Actor not found")

    return {"status": "deleted"}