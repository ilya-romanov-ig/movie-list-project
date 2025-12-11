from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class FavoriteFilm(Base):
    __tablename__ = "favorite_films"

    user_id = Column(Integer, ForeignKey("app_users.user_id", ondelete="CASCADE"), primary_key=True)
    film_id = Column(Integer, ForeignKey("films.film_id", ondelete="CASCADE"), primary_key=True)

    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites_films")
    film = relationship("Film", back_populates="favorites")
