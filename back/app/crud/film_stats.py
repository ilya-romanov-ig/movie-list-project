# app/crud/film_stats.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.film_stats import FilmStats


async def get_film_stats(session: AsyncSession, film_id: int) -> FilmStats | None:
    stmt = select(FilmStats).where(FilmStats.film_id == film_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()
