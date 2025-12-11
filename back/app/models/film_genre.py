from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from app.db import Base

class FilmGenre(Base):
    __tablename__ = "film_genres"

    film_id = Column(Integer, ForeignKey("films.film_id", ondelete="CASCADE"), primary_key=True)
    genre_id = Column(Integer, ForeignKey("genres.genre_id", ondelete="CASCADE"), primary_key=True)

    film = relationship("Film", back_populates="genres")
    genre = relationship("Genre", back_populates="films")

    __table_args__ = (
        UniqueConstraint("film_id", "genre_id"),
    )
