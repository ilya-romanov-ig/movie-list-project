# app/routers/films.py
from sqlalchemy import select
from typing import List, Optional
from app.models.film import Film
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db

from app.crud.films import (
    get_film_by_id,
    list_films,
    get_top_by_rating,
    get_newest,
    get_actors_for_film
)
from app.crud.genres import get_genres_for_film
from app.crud.ratings import get_ratings_for_film, get_avg_rating

from app.crud.film_stats import get_film_stats

router = APIRouter(prefix="/films", tags=["Films"])


# --------------------------
# GET /films/top
# --------------------------
@router.get("/top")
async def top_films(db: AsyncSession = Depends(get_db)):
    films = await get_top_by_rating(db, limit=5)
    return {
        "count": len(films),
        "items": [{"id": f.film_id, "title": f.title} for f in films]
    }

# --------------------------
# GET /films/newest
# --------------------------
@router.get("/newest")
async def newest_films(db: AsyncSession = Depends(get_db)):
    films = await get_newest(db, limit=10)
    return {
        "count": len(films),
        "items": [{"id": f.film_id, "title": f.title} for f in films]
    }


# --------------------------
# GET /films/{film_id}
# --------------------------
@router.get("/{film_id}")
async def film_details(film_id: int, db: AsyncSession = Depends(get_db)):
    film = await get_film_by_id(db, film_id)
    if not film:
        raise HTTPException(404, "Film not found")

    return {
        "id": film.film_id,
        "title": film.title,
        "year": film.year,
        "description": film.description,
        "runtime": film.runtime,
        "poster_url": film.poster_url,
    }


# --------------------------
# GET /films/{film_id}/actors
# --------------------------
@router.get("/{film_id}/actors")
async def film_actors(film_id: int, db: AsyncSession = Depends(get_db)):
    actors = await get_actors_for_film(db, film_id)
    return {
        "count": len(actors),
        "items": [
            {"actor_id": a.actor_id, "name": a.name}
            for a in actors
        ],
    }


# --------------------------
# GET /films/{film_id}/genres
# --------------------------
@router.get("/{film_id}/genres")
async def film_genres(film_id: int, db: AsyncSession = Depends(get_db)):
    genres = await get_genres_for_film(db, film_id)
    return {
        "count": len(genres),
        "items": [
            {"genre_id": g.genre_id, "name": g.name}
            for g in genres
        ],
    }


# --------------------------
# GET /films/{film_id}/ratings
# --------------------------
@router.get("/{film_id}/ratings")
async def film_ratings(film_id: int, db: AsyncSession = Depends(get_db)):
    ratings = await get_ratings_for_film(db, film_id)
    return {
        "count": len(ratings),
        "items": [
            {"user_id": r.user_id, "rating": r.rating}
            for r in ratings
        ],
    }


# --------------------------
# GET /films/{film_id}/rating
# --------------------------
@router.get("/{film_id}/rating")
async def film_avg_rating(film_id: int, db: AsyncSession = Depends(get_db)):
    value = await get_avg_rating(db, film_id)
    return {"film_id": film_id, "avg_rating": value}








@router.get("/{film_id}/details")
async def get_film_details(
    film_id: int,
    db: AsyncSession = Depends(get_db)
):
    film = await get_film_by_id(db, film_id)
    if not film:
        raise HTTPException(404, "Film not found")

    actors = await get_actors_for_film(db, film_id)
    genres = await get_genres_for_film(db, film_id)
    stats = await get_film_stats(db, film_id)

    return {
        "film_id": film.film_id,
        "title": film.title,
        "release_year": film.year,
        "description": film.description,
        "runtime": film.runtime,
        "poster_url": film.poster_url,
        "genres": [{"id": g.genre_id, "name": g.name} for g in genres],
        "actors": [{"id": a.actor_id, "name": a.name} for a in actors],
        "stats": {
            "avg_rating": stats.avg_rating if stats else None,
            "ratings_count": stats.n_ratings if stats else 0,
            "watched_count": stats.watched_count if stats else 0,
            "updated_at": stats.updated_at if stats else None
        }
    }


