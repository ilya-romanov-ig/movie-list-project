# app/routers/home.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.db import get_db
from app.clients.ml_client import ml_client  # Импортируем клиент
from app.security.jwt import get_optional_user, get_current_user
from app.models.user import User

router = APIRouter(prefix="/home", tags=["Home"])

# --------------------------
# Вспомогательные функции
# --------------------------

async def get_ml_recommendations(user_id: int, limit: int = 10) -> List[int]:
    """Получить рекомендации от ML-сервиса"""
    try:
        # Проверяем доступность ML-сервиса
        is_healthy = await ml_client.health_check()
        
        if not is_healthy:
            # Fallback: возвращаем пустой список или популярные фильмы
            return []
        
        # Получаем рекомендации
        film_ids = await ml_client.get_recommendations(user_id, count=limit)
        return film_ids
    except Exception as e:
        # Логируем ошибку, но не падаем
        print(f"Ошибка получения рекомендаций: {e}")
        return []

async def get_films_by_ids(db: AsyncSession, film_ids: List[int]):
    """Получить фильмы по списку ID"""
    if not film_ids:
        return []
    
    # Импортируем здесь, чтобы избежать циклических импортов
    from app.crud.films import get_films_by_ids as crud_get_films_by_ids
    return await crud_get_films_by_ids(db, film_ids)

def format_films(films):
    """Форматирование списка фильмов"""
    return [{
        "id": f.film_id,
        "title": f.title,
        "poster_url": f.poster_url if hasattr(f, 'poster_url') else None,
        "rating": f.rating if hasattr(f, 'rating') else None,
        "year": f.year if hasattr(f, 'year') else None
    } for f in films]

# --------------------------
# Импортируем функции из других модулей
# --------------------------

# Если эти функции в другом модуле, импортируем их
# Вместо этого можно импортировать из вашего существующего модуля
try:
    from app.crud.films import get_top_by_rating, get_newest, get_recommended_stub
except ImportError:
    # Создаем заглушки, если модуль не найден
    async def get_top_by_rating(db, limit=10):
        return []
    
    async def get_newest(db, limit=10):
        return []
    
    async def get_recommended_stub(db, user_id=None, limit=10):
        return []

# --------------------------
# Эндпоинты
# --------------------------

@router.get("")
async def home_page(
    current_user: Optional[User] = Depends(get_optional_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id if current_user else None
    
    # Получаем данные из БД
    top = await get_top_by_rating(db, limit=5)
    newest = await get_newest(db, limit=8)
    
    # Получаем рекомендации
    if user_id:
        # Персональные рекомендации от ML
        recommended_film_ids = await get_ml_recommendations(user_id, limit=8)
        # Получаем детали фильмов по ID
        recommended_films = await get_films_by_ids(db, recommended_film_ids)
    else:
        # Для неавторизованных - популярные
        recommended_films = top[:8]
    
    # Trending (можно использовать популярные)
    trending_films = top[:5]
    
    return {
        "top_films": {"items": format_films(top)},
        "newest_films": {"items": format_films(newest)},
        "recommended": {"items": format_films(recommended_films)},
        "trending": {"items": format_films(trending_films)}
    }

@router.get("/recommended")
async def recommended(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_id = current_user.user_id
    
    # Получаем рекомендации от ML-сервиса
    recommended_film_ids = await get_ml_recommendations(user_id, limit=10)
    
    # Получаем детали фильмов
    films = await get_films_by_ids(db, recommended_film_ids)
    
    return {
        "items": format_films(films),
        "source": "ml_service"
    }

@router.get("/trending")
async def trending(db: AsyncSession = Depends(get_db)):
    films = await get_top_by_rating(db, limit=10)
    return {"items": format_films(films)}