# app/routers/home.py

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.films import (
    get_top_by_rating,
    get_newest,
    get_recommended_stub
)

router = APIRouter(prefix="/home", tags=["Home"])


# --------------------------
# GET /home
# Главная страница
# --------------------------
@router.get("")
async def home_page(
    user_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    top = await get_top_by_rating(db, limit=5)
    newest = await get_newest(db, limit=8)
    recommended = await get_recommended_stub(db, user_id=user_id, limit=8)

    return {
        "top_films": [
            {"id": f.film_id, "title": f.title} for f in top
        ],
        "newest_films": [
            {"id": f.film_id, "title": f.title} for f in newest
        ],
        "recommended": [
            {"id": f.film_id, "title": f.title} for f in recommended
        ]
    }


# --------------------------
# GET /home/recommended
# --------------------------
@router.get("/recommended")
async def recommended(
    user_id: int | None = None,
    db: AsyncSession = Depends(get_db)
):
    films = await get_recommended_stub(db, user_id=user_id, limit=10)
    return {"items": [{"id": f.film_id, "title": f.title} for f in films]}


# --------------------------
# GET /home/trending
# --------------------------
@router.get("/trending")
async def trending(db: AsyncSession = Depends(get_db)):
    films = await get_top_by_rating(db, limit=10)
    return {"items": [{"id": f.film_id, "title": f.title} for f in films]}
