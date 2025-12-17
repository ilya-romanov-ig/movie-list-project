# app/deps.py

from fastapi import Depends, HTTPException
from app.db import async_session
from app.security.jwt import get_current_user as _get_current_user
from sqlalchemy.ext.asyncio import AsyncSession


# DB session dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session


# Current user dependency (обертка)
async def get_current_user(
    user = Depends(_get_current_user)
):
    return user


# Optional user (если пользователь может быть не авторизован)
async def get_optional_user(
    user = Depends(_get_current_user, use_cache=True)
):
    return user
