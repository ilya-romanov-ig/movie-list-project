from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.db import Base


class FilmActor(Base):
    __tablename__ = "film_actors"

    id = Column(Integer, primary_key=True)

    film_id = Column(Integer, ForeignKey("films.film_id", ondelete="CASCADE"))
    actor_id = Column(String, ForeignKey("actors.actor_id", ondelete="CASCADE"))  # было Integer

    role_name = Column(String, nullable=True)

    film = relationship("Film", back_populates="actors")
    actor = relationship("Actor", back_populates="films")
