# app/crud/genres.py
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.genre import Genre
from app.models.film_genre import FilmGenre
from app.models.film import Film


# -------------------------------------------------------
# GET ONE
# -------------------------------------------------------
async def get_genre_by_id(session: AsyncSession, genre_id: int) -> Optional[Genre]:
    return await session.get(Genre, genre_id)


# -------------------------------------------------------
# LIST / FILTER
# -------------------------------------------------------
async def list_genres(
    session: AsyncSession,
    *,
    limit: int = 50,
    offset: int = 0,
    name_query: Optional[str] = None,
) -> List[Genre]:
    stmt = select(Genre)

    if name_query:
        stmt = stmt.where(Genre.name.ilike(f"%{name_query}%"))

    stmt = stmt.limit(limit).offset(offset)

    result = await session.execute(stmt)
    return result.scalars().all()


# -------------------------------------------------------
# CREATE
# -------------------------------------------------------
async def create_genre(session: AsyncSession, *, name: str) -> Genre:
    genre = Genre(name=name)
    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre


# -------------------------------------------------------
# UPDATE
# -------------------------------------------------------
async def update_genre(
    session: AsyncSession,
    genre_id: int,
    *,
    name: Optional[str] = None,
) -> Optional[Genre]:
    genre = await get_genre_by_id(session, genre_id)
    if not genre:
        return None

    if name is not None:
        genre.name = name

    session.add(genre)
    await session.commit()
    await session.refresh(genre)
    return genre


# -------------------------------------------------------
# DELETE
# -------------------------------------------------------
async def delete_genre(session: AsyncSession, genre_id: int) -> bool:
    genre = await get_genre_by_id(session, genre_id)
    if not genre:
        return False

    await session.delete(genre)
    await session.commit()
    return True


# -------------------------------------------------------
# GET GENRES OF FILM  (ты уже делал)
# -------------------------------------------------------
async def get_genres_for_film(session: AsyncSession, film_id: int) -> List[Genre]:
    stmt = (
        select(Genre)
        .join(FilmGenre, Genre.genre_id == FilmGenre.genre_id)
        .where(FilmGenre.film_id == film_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


# -------------------------------------------------------
# GET FILMS OF GENRE
# -------------------------------------------------------
async def get_films_of_genre(session: AsyncSession, genre_id: int) -> List[Film]:
    stmt = (
        select(Film)
        .join(FilmGenre, Film.film_id == FilmGenre.film_id)
        .where(FilmGenre.genre_id == genre_id)
    )
    result = await session.execute(stmt)
    return result.scalars().unique().all()
