# app/crud/ratings.py

from typing import List, Optional
from sqlalchemy import select, func, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rating import Rating


# -------------------------
# GET: all ratings for film
# -------------------------
async def get_ratings_for_film(session: AsyncSession, film_id: int) -> List[Rating]:
    stmt = select(Rating).where(Rating.film_id == film_id)
    result = await session.execute(stmt)
    return result.scalars().all()


# -------------------------
# GET: average rating
# -------------------------
async def get_avg_rating(session: AsyncSession, film_id: int) -> Optional[float]:
    stmt = select(func.avg(Rating.rating)).where(Rating.film_id == film_id)
    result = await session.execute(stmt)
    return result.scalar()


# -------------------------
# SET / UPDATE rating
# -------------------------
async def set_rating(
    session: AsyncSession,
    user_id: int,
    film_id: int,
    rating_value: int,
) -> Rating:

    # Проверяем: уже есть рейтинг?
    stmt = select(Rating).where(
        Rating.user_id == user_id,
        Rating.film_id == film_id
    )
    result = await session.execute(stmt)
    existing = result.scalar_one_or_none()

    if existing:
        # обновляем
        existing.rating = rating_value
        session.add(existing)
        await session.commit()
        await session.refresh(existing)
        return existing

    # создаём новый
    new_rating = Rating(
        user_id=user_id,
        film_id=film_id,
        rating=rating_value
    )
    session.add(new_rating)
    await session.commit()
    await session.refresh(new_rating)
    return new_rating


# -------------------------
# DELETE rating
# -------------------------
async def delete_rating(session: AsyncSession, user_id: int, film_id: int) -> bool:
    stmt = delete(Rating).where(
        Rating.user_id == user_id,
        Rating.film_id == film_id
    )

    result = await session.execute(stmt)
    await session.commit()

    return result.rowcount > 0
