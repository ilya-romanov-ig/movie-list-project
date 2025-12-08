from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.actor import Actor
from app.models.film_actor import FilmActor
from app.models.film import Film


# -----------------------
# Basic getters
# -----------------------

async def get_actor_by_id(session: AsyncSession, actor_id: str) -> Optional[Actor]:
    return await session.get(Actor, actor_id)


async def list_actors(
    session: AsyncSession,
    *,
    limit: int = 20,
    offset: int = 0,
    name_query: Optional[str] = None,
) -> List[Actor]:
    stmt = select(Actor)

    if name_query:
        stmt = stmt.where(Actor.name.ilike(f"%{name_query}%"))

    stmt = stmt.limit(limit).offset(offset)
    result = await session.execute(stmt)
    return result.scalars().all()


# -----------------------
# Create
# -----------------------

async def create_actor(
    session: AsyncSession,
    *,
    actor_id: str,
    name: str,
    bio: Optional[str] = None,
    birth_year: Optional[int] = None,
    photo_url: Optional[str] = None,
) -> Actor:
    actor = Actor(
        actor_id=actor_id,
        name=name,
        bio=bio,
        birth_year=birth_year,
        photo_url=photo_url,
    )

    session.add(actor)
    await session.commit()
    await session.refresh(actor)
    return actor


# -----------------------
# Update
# -----------------------

async def update_actor(
    session: AsyncSession,
    actor_id: str,
    *,
    name: Optional[str] = None,
    bio: Optional[str] = None,
    birth_year: Optional[int] = None,
    photo_url: Optional[str] = None,
) -> Optional[Actor]:

    actor = await get_actor_by_id(session, actor_id)
    if not actor:
        return None

    if name is not None:
        actor.name = name
    if bio is not None:
        actor.bio = bio
    if birth_year is not None:
        actor.birth_year = birth_year
    if photo_url is not None:
        actor.photo_url = photo_url

    session.add(actor)
    await session.commit()
    await session.refresh(actor)
    return actor


# -----------------------
# Delete
# -----------------------

async def delete_actor(session: AsyncSession, actor_id: str) -> bool:
    actor = await get_actor_by_id(session, actor_id)
    if not actor:
        return False

    await session.delete(actor)
    await session.commit()
    return True


# -----------------------
# Films of actor
# -----------------------

async def get_films_of_actor(
    session: AsyncSession, actor_id: str, limit: int = 50
) -> List[Film]:
    stmt = (
        select(Film)
        .join(FilmActor, Film.film_id == FilmActor.film_id)
        .where(FilmActor.actor_id == actor_id)
        .limit(limit)
    )

    result = await session.execute(stmt)
    return result.scalars().unique().all()
