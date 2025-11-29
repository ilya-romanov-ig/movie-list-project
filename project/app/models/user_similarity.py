from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.db import Base

class UserSimilarity(Base):
    __tablename__ = "user_similarity"

    user_a = Column(Integer, ForeignKey("app_users.user_id", ondelete="CASCADE"), primary_key=True)
    user_b = Column(Integer, ForeignKey("app_users.user_id", ondelete="CASCADE"), primary_key=True)

    score = Column(Float, nullable=False)
    computed_at = Column(DateTime(timezone=True), server_default=func.now())
