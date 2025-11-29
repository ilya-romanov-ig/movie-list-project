# app/crud/search.py

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.film import Film
from app.models.actor import Actor
from app.models.genre import Genre
from app.models.user import User

async def search_films(session: AsyncSession, query: str, limit: int = 10):
    stmt = (
        select(Film)
        .where(Film.title.ilike(f"%{query}%"))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def search_actors(session: AsyncSession, query: str, limit: int = 10):
    stmt = (
        select(Actor)
        .where(Actor.name.ilike(f"%{query}%"))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def search_users(session: AsyncSession, query: str, limit: int = 10):
    stmt = (
        select(User)
        .where(User.username.ilike(f"%{query}%"))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()
