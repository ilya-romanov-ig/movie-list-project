# app/routers/watched.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.watched import (
    mark_watched,
    unmark_watched,
    get_watched,
)

router = APIRouter(prefix="/watched", tags=["Watched"])


@router.post("/{film_id}")
async def mark_film_watched(
    film_id: int,
    user_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    await mark_watched(db, user_id=user_id, film_id=film_id)
    return {"status": "watched", "film_id": film_id}


@router.delete("/{film_id}")
async def unmark_film_watched(
    film_id: int,
    user_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    ok = await unmark_watched(db, user_id=user_id, film_id=film_id)
    if not ok:
        raise HTTPException(404, "Film was not marked as watched")

    return {"status": "unmarked", "film_id": film_id}


@router.get("")
async def list_watched(
    user_id: int = Query(...),
    db: AsyncSession = Depends(get_db),
):
    films = await get_watched(db, user_id)
    return {"count": len(films), "film_ids": films}
