from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime


class FilmStats(Base):
    __tablename__ = "film_stats"

    film_id = Column(Integer, ForeignKey("films.film_id", ondelete="CASCADE"), primary_key=True)

    avg_rating = Column(Float, nullable=True)
    n_ratings = Column(Integer, nullable=True)
    watched_count = Column(Integer, nullable=True)

    updated_at = Column(DateTime(timezone=True))  # ← ВАЖНО!!!

    film = relationship("Film", back_populates="stats")
