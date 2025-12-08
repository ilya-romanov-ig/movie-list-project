from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db import Base


class Film(Base):
    __tablename__ = "films"

    film_id = Column(Integer, primary_key=True, index=True)
    imdb_tconst = Column(String)
    tmdb_id = Column(Integer)
    title = Column(String, nullable=False)
    year = Column(Integer)
    description = Column(Text)
    runtime = Column(Integer)
    poster_url = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    search_vector = Column(Text)

    actors = relationship("FilmActor", back_populates="film", cascade="all, delete-orphan")
    genres = relationship("FilmGenre", back_populates="film", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="film", cascade="all, delete-orphan")
    watched_by = relationship("WatchedFilm", back_populates="film", cascade="all, delete-orphan")
    favorites = relationship("FavoriteFilm", back_populates="film", cascade="all, delete-orphan")

    # главное — связь со статистикой
    stats = relationship("FilmStats", back_populates="film", uselist=False)
