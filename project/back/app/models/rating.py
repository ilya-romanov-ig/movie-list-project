from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class Rating(Base):
    __tablename__ = "ratings"

    user_id = Column(Integer, ForeignKey("app_users.user_id", ondelete="CASCADE"), primary_key=True)
    film_id = Column(Integer, ForeignKey("films.film_id", ondelete="CASCADE"), primary_key=True)

    rating = Column(Integer, nullable=False)
    rated_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="ratings")
    film = relationship("Film", back_populates="ratings")
