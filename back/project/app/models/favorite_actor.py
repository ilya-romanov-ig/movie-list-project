from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db import Base


class FavoriteActor(Base):
    __tablename__ = "favorite_actors"

    user_id = Column(Integer, ForeignKey("app_users.user_id", ondelete="CASCADE"), primary_key=True)

    # теперь строковый, как и в Actor
    actor_id = Column(String, ForeignKey("actors.actor_id", ondelete="CASCADE"), primary_key=True)

    added_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="favorites_actors")
    actor = relationship("Actor", back_populates="favorites")
