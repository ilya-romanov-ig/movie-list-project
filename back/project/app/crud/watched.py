# app/crud/watched.py

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.watched import WatchedFilm


async def mark_watched(session: AsyncSession, user_id: int, film_id: int):
    watch = WatchedFilm(user_id=user_id, film_id=film_id)
    session.add(watch)
    await session.commit()
    return True


async def unmark_watched(session: AsyncSession, user_id: int, film_id: int):
    stmt = delete(WatchedFilm).where(
        WatchedFilm.user_id == user_id,
        WatchedFilm.film_id == film_id
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def get_watched(session: AsyncSession, user_id: int):
    stmt = select(WatchedFilm.film_id).where(WatchedFilm.user_id == user_id)
    result = await session.execute(stmt)
    return [row for (row,) in result.all()]
