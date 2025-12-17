# app/routers/watched.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.watched import (
    mark_watched,
    unmark_watched,
    get_watched,
)
from app.security.jwt import get_current_user
from app.models.user import User

router = APIRouter(prefix="/watched", tags=["Watched"])


@router.post("/{film_id}")
async def mark_film_watched(
    film_id: int,
    current_user: User = Depends(get_current_user),  # <- Получаем из JWT
    db: AsyncSession = Depends(get_db),
):
    await mark_watched(db, user_id=current_user.user_id, film_id=film_id)
    return {"status": "watched", "film_id": film_id}


@router.delete("/{film_id}")
async def unmark_film_watched(
    film_id: int,
    current_user: User = Depends(get_current_user),  # <- Получаем из JWT
    db: AsyncSession = Depends(get_db),
):
    ok = await unmark_watched(db, user_id=current_user.user_id, film_id=film_id)
    if not ok:
        raise HTTPException(404, "Film was not marked as watched")

    return {"status": "unmarked", "film_id": film_id}


@router.get("")
async def list_watched(
    current_user: User = Depends(get_current_user),  # <- Получаем из JWT
    db: AsyncSession = Depends(get_db),
):
    films = await get_watched(db, current_user.user_id)
    return {"count": len(films), "film_ids": films}