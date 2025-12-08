# app/routers/genres.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.genres import (
    list_genres,
    get_genre_by_id,
    create_genre,
    update_genre,
    delete_genre,
    get_films_of_genre,
)

router = APIRouter(prefix="/genres", tags=["Genres"])


# ----------------------------------------------------------
# GET /genres — список жанров
# ----------------------------------------------------------
@router.get("")
async def get_all_genres(
    db: AsyncSession = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
    name: str | None = None,
):
    genres = await list_genres(db, limit=limit, offset=offset, name_query=name)
    return {
        "count": len(genres),
        "items": [
            {"genre_id": g.genre_id, "name": g.name}
            for g in genres
        ]
    }


# ----------------------------------------------------------
# GET /genres/{genre_id} — детали жанра
# ----------------------------------------------------------
@router.get("/{genre_id}")
async def get_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    genre = await get_genre_by_id(db, genre_id)
    if not genre:
        raise HTTPException(404, "Genre not found")

    return {
        "genre_id": genre.genre_id,
        "name": genre.name,
    }


# ----------------------------------------------------------
# GET /genres/{genre_id}/films — фильмы жанра
# ----------------------------------------------------------
@router.get("/{genre_id}/films")
async def get_genre_films(genre_id: int, db: AsyncSession = Depends(get_db)):
    films = await get_films_of_genre(db, genre_id)
    return {
        "count": len(films),
        "items": [
            {"film_id": f.film_id, "title": f.title}
            for f in films
        ]
    }


# ----------------------------------------------------------
# POST /genres — создать жанр
# ----------------------------------------------------------
@router.post("")
async def create_new_genre(
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    if not data.get("name"):
        raise HTTPException(400, "Field 'name' is required")

    genre = await create_genre(db, name=data["name"])

    return {"status": "created", "genre_id": genre.genre_id}


# ----------------------------------------------------------
# PATCH /genres/{genre_id} — обновить жанр
# ----------------------------------------------------------
@router.patch("/{genre_id}")
async def edit_genre(
    genre_id: int,
    data: dict,
    db: AsyncSession = Depends(get_db),
):
    genre = await update_genre(db, genre_id, name=data.get("name"))

    if not genre:
        raise HTTPException(404, "Genre not found")

    return {"status": "updated"}


# ----------------------------------------------------------
# DELETE /genres/{genre_id}
# ----------------------------------------------------------
@router.delete("/{genre_id}")
async def remove_genre(genre_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_genre(db, genre_id)

    if not ok:
        raise HTTPException(404, "Genre not found")

    return {"status": "deleted"}
