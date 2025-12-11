from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.db import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import JSONB
class User(Base):
    __tablename__ = "app_users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    password_hash = Column(String, nullable=False)

    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    socials = Column(JSONB, nullable=True, default=dict)

    is_private = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # связи — пока пустые, потом добавим
    favorites_films = relationship("FavoriteFilm", back_populates="user")
    favorites_actors = relationship("FavoriteActor", back_populates="user")

    ratings = relationship("Rating", back_populates="user")
    watched = relationship("WatchedFilm", back_populates="user", cascade="all, delete-orphan")

