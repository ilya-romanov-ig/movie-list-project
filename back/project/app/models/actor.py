from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from app.db import Base


class Actor(Base):
    __tablename__ = "actors"

    actor_id = Column(String, primary_key=True, index=True)   # было Integer → теперь str
    name = Column(String, nullable=False)
    birth_year = Column(Integer)
    death_year = Column(Integer)
    photo_url = Column(String)
    bio = Column(Text)     # в БД поле называется bio

    # relationships
    films = relationship("FilmActor", back_populates="actor", cascade="all, delete-orphan")
    favorites = relationship("FavoriteActor", back_populates="actor", cascade="all, delete-orphan")
