# app/crud/favorites.py

from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.favorite_film import FavoriteFilm
from app.models.favorite_actor import FavoriteActor
from app.models.film import Film
from app.models.actor import Actor


# ------------------------------------------
# FAVORITE FILMS
# ------------------------------------------

async def add_favorite_film(session: AsyncSession, user_id: int, film_id: int):
    fav = FavoriteFilm(user_id=user_id, film_id=film_id)
    session.add(fav)
    await session.commit()
    return True


async def remove_favorite_film(session: AsyncSession, user_id: int, film_id: int):
    stmt = delete(FavoriteFilm).where(
        FavoriteFilm.user_id == user_id,
        FavoriteFilm.film_id == film_id
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def get_favorite_films(session: AsyncSession, user_id: int) -> List[Film]:
    stmt = (
        select(Film)
        .join(FavoriteFilm, Film.film_id == FavoriteFilm.film_id)
        .where(FavoriteFilm.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def is_film_favorite(session: AsyncSession, user_id: int, film_id: int) -> bool:
    stmt = (
        select(FavoriteFilm)
        .where(FavoriteFilm.user_id == user_id,
               FavoriteFilm.film_id == film_id)
    )
    result = await session.execute(stmt)
    return result.scalar() is not None


# ------------------------------------------
# FAVORITE ACTORS
# ------------------------------------------

async def add_favorite_actor(session: AsyncSession, user_id: int, actor_id: int):
    fav = FavoriteActor(user_id=user_id, actor_id=actor_id)
    session.add(fav)
    await session.commit()
    return True


async def remove_favorite_actor(session: AsyncSession, user_id: int, actor_id: int):
    stmt = delete(FavoriteActor).where(
        FavoriteActor.user_id == user_id,
        FavoriteActor.actor_id == actor_id
    )
    result = await session.execute(stmt)
    await session.commit()
    return result.rowcount > 0


async def get_favorite_actors(session: AsyncSession, user_id: int) -> List[Actor]:
    stmt = (
        select(Actor)
        .join(FavoriteActor, Actor.actor_id == FavoriteActor.actor_id)
        .where(FavoriteActor.user_id == user_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def is_actor_favorite(session: AsyncSession, user_id: int, actor_id: int) -> bool:
    stmt = (
        select(FavoriteActor)
        .where(FavoriteActor.user_id == user_id,
               FavoriteActor.actor_id == actor_id)
    )
    result = await session.execute(stmt)
    return result.scalar() is not None
