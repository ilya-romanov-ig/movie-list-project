# app/crud/films.py
from typing import List, Optional, Tuple
from sqlalchemy import select, update, delete, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.film import Film
from app.models.film_genre import FilmGenre
from app.models.film_stats import FilmStats
from app.models.film_actor import FilmActor
from app.models.genre import Genre
from app.models.actor import Actor


# -----------------------
# Basic getters / helpers
# -----------------------
async def get_film_by_id(session: AsyncSession, film_id: int) -> Optional[Film]:
    """Return Film by id or None."""
    return await session.get(Film, film_id)


# -----------------------
# List / filters / sorting
# -----------------------
async def list_films(
    session: AsyncSession,
    *,
    limit: int = 20,
    offset: int = 0,
    genre_id: Optional[int] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    min_rating: Optional[float] = None,
    sort_by: str = "release_year",  # "rating", "watched", "release_year", "created"
    sort_desc: bool = True,
) -> List[Film]:
    """
    Returns list of Film objects applying optional filters and sorting.
    - genre_id: filter by genre
    - year_from/year_to: filter by release_year
    - min_rating: filter by avg rating from film_stats
    - sort_by: one of 'rating','watched','release_year','created'
    """

    # base select from films
    stmt = select(Film)

    # join film_stats if needed (filter or sort by rating/watched)
    if min_rating is not None or sort_by in ("rating", "watched"):
        stmt = stmt.join(FilmStats, Film.film_id == FilmStats.film_id, isouter=True)

    # filter by genre
    if genre_id is not None:
        # join through film_genre
        stmt = stmt.join(FilmGenre, Film.film_id == FilmGenre.film_id).where(FilmGenre.genre_id == genre_id)

    # year filters
    if year_from is not None:
        stmt = stmt.where(Film.release_year >= year_from)
    if year_to is not None:
        stmt = stmt.where(Film.release_year <= year_to)

    # min_rating filter
    if min_rating is not None:
        stmt = stmt.where(FilmStats.avg_rating >= min_rating)

    # sorting
    if sort_by == "rating":
        order_col = FilmStats.avg_rating
    elif sort_by == "watched":
        order_col = FilmStats.watched_count
    elif sort_by == "created":
        # assume Film has created_at
        order_col = Film.created_at
    else:
        order_col = Film.release_year

    if sort_desc:
        stmt = stmt.order_by(desc(order_col.nullsfirst()))
    else:
        stmt = stmt.order_by(asc(order_col.nullslast()))

    stmt = stmt.limit(limit).offset(offset)

    result = await session.execute(stmt)
    films = result.scalars().unique().all()
    return films


# -----------------------
# Create / Update / Delete
# -----------------------
async def create_film(
    session: AsyncSession,
    *,
    title: str,
    release_year: int,
    runtime: Optional[int] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
) -> Film:
    """Create new film row and return it (SQLAlchemy model)."""
    film = Film(
        title=title,
        release_year=release_year,
        runtime=runtime,
        description=description,
        poster_url=poster_url,
    )
    session.add(film)
    await session.commit()
    await session.refresh(film)
    return film


async def update_film(
    session: AsyncSession,
    film_id: int,
    *,
    title: Optional[str] = None,
    release_year: Optional[int] = None,
    runtime: Optional[int] = None,
    description: Optional[str] = None,
    poster_url: Optional[str] = None,
) -> Optional[Film]:
    """Partial update of film. Returns updated Film or None if not found."""
    film = await get_film_by_id(session, film_id)
    if not film:
        return None

    if title is not None:
        film.title = title
    if release_year is not None:
        film.release_year = release_year
    if runtime is not None:
        film.runtime = runtime
    if description is not None:
        film.description = description
    if poster_url is not None:
        film.poster_url = poster_url

    session.add(film)
    await session.commit()
    await session.refresh(film)
    return film


async def delete_film(session: AsyncSession, film_id: int) -> bool:
    """Delete film by id. Returns True if deleted, False if not found."""
    film = await get_film_by_id(session, film_id)
    if not film:
        return False
    await session.delete(film)
    await session.commit()
    return True

async def get_films_by_ids(
    db: AsyncSession, 
    film_ids: List[int], 
    limit: Optional[int] = None
) -> List[Film]:
    """Получить фильмы по списку ID"""
    if not film_ids:
        return []
    
    query = select(Film).where(Film.film_id.in_(film_ids))
    
    if limit:
        query = query.limit(limit)
    
    result = await db.execute(query)
    films = result.scalars().all()
    
    # Сохраняем порядок из film_ids
    film_dict = {film.film_id: film for film in films}
    ordered_films = [film_dict[film_id] for film_id in film_ids if film_id in film_dict]
    
    return ordered_films

# -----------------------
# Extra useful queries
# -----------------------
async def get_top_by_rating(session: AsyncSession, limit: int = 10) -> List[Film]:
    """Return top films by avg_rating (uses film_stats)."""
    stmt = (
        select(Film)
        .join(FilmStats, Film.film_id == FilmStats.film_id)
        .order_by(FilmStats.avg_rating.desc().nullslast())
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_newest(session: AsyncSession, limit: int = 10) -> List[Film]:
    """Return newest by created_at / id fallback."""
    # prefer created_at if exists
    if hasattr(Film, "created_at"):
        stmt = select(Film).order_by(desc(Film.created_at)).limit(limit)
    else:
        stmt = select(Film).order_by(desc(Film.film_id)).limit(limit)
    result = await session.execute(stmt)
    return result.scalars().all()


async def get_films_by_actor(session: AsyncSession, actor_id: int, limit: int = 50) -> List[Film]:
    """Return films for actor (via film_actor)."""
    stmt = (
        select(Film)
        .join(FilmActor, Film.film_id == FilmActor.film_id)
        .where(FilmActor.actor_id == actor_id)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().unique().all()


async def get_films_by_genre(session: AsyncSession, genre_id: int, limit: int = 50) -> List[Film]:
    """Return films for genre (via film_genre)."""
    stmt = (
        select(Film)
        .join(FilmGenre, Film.film_id == FilmGenre.film_id)
        .where(FilmGenre.genre_id == genre_id)
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().unique().all()


# -----------------------
# Recommendation stub (simple)
# -----------------------
async def get_recommended_stub(session: AsyncSession, user_id: Optional[int] = None, limit: int = 10) -> List[Film]:
    """
    Temporary recommendations stub:
    - if user_id provided: return newest films (placeholder)
    - else: return top by rating
    """
    if user_id is None:
        return await get_top_by_rating(session, limit=limit)
    else:
        return await get_newest(session, limit=limit)



async def get_actors_for_film(session: AsyncSession, film_id: int) -> List[Actor]:
    stmt = (
        select(Actor)
        .join(FilmActor, Actor.actor_id == FilmActor.actor_id)
        .where(FilmActor.film_id == film_id)
    )
    result = await session.execute(stmt)
    return result.scalars().all()



