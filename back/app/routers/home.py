# app/routers/home.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.films import (
    get_top_by_rating,
    get_newest,
    get_recommended_stub
)
from app.security.jwt import get_current_user
from app.models.user import User

router = APIRouter(prefix="/home", tags=["Home"])


# --------------------------
# GET /home
# Главная страница
# --------------------------
@router.get("")
async def home_page(
    current_user: User = Depends(get_current_user),  # <- JWT
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id if current_user else None
    
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
    current_user: User = Depends(get_current_user),  # <- JWT
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id if current_user else None
    films = await get_recommended_stub(db, user_id=user_id, limit=10)
    return {"items": [{"id": f.film_id, "title": f.title} for f in films]}


# --------------------------
# GET /home/trending
# --------------------------
@router.get("/trending")
async def trending(db: AsyncSession = Depends(get_db)):
    films = await get_top_by_rating(db, limit=10)
    return {"items": [{"id": f.film_id, "title": f.title} for f in films]}