# app/routers/ratings.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.ratings import (
    get_ratings_for_film,
    get_avg_rating,
    set_rating,
    delete_rating
)
from app.security.jwt import get_current_user
from app.models.user import User

router = APIRouter(prefix="/ratings", tags=["Ratings"])


# -------------------------
# GET /ratings/{film_id}
# -------------------------
@router.get("/{film_id}")
async def list_film_ratings(
    film_id: int,
    db: AsyncSession = Depends(get_db)
):
    ratings = await get_ratings_for_film(db, film_id)
    return {
        "count": len(ratings),
        "items": [
            {"user_id": r.user_id, "rating": r.rating}
            for r in ratings
        ]
    }


# -------------------------
# GET /ratings/{film_id}/avg
# -------------------------
@router.get("/{film_id}/avg")
async def avg_rating(
    film_id: int,
    db: AsyncSession = Depends(get_db)
):
    avg = await get_avg_rating(db, film_id)
    return {"film_id": film_id, "avg_rating": avg}


# -------------------------
# POST /ratings/{film_id}
# -------------------------
@router.post("/{film_id}")
async def rate_film(
    film_id: int,
    rating: int = Query(..., ge=1, le=10),
    current_user: User = Depends(get_current_user),  # <- JWT вместо user_id
    db: AsyncSession = Depends(get_db),
):
    updated = await set_rating(
        db, 
        user_id=current_user.user_id, 
        film_id=film_id, 
        rating_value=rating
    )
    return {"status": "ok", "film_id": film_id, "rating": updated.rating}


# -------------------------
# DELETE /ratings/{film_id}
# -------------------------
@router.delete("/{film_id}")
async def remove_rating(
    film_id: int,
    current_user: User = Depends(get_current_user),  # <- JWT вместо user_id
    db: AsyncSession = Depends(get_db)
):
    ok = await delete_rating(db, current_user.user_id, film_id)
    if not ok:
        raise HTTPException(404, "Rating not found")

    return {"status": "deleted", "film_id": film_id}