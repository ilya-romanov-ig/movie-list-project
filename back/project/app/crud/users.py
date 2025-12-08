# app/crud/users.py

from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


async def get_user_by_id(session: AsyncSession, user_id: int) -> Optional[User]:
    return await session.get(User, user_id)


async def get_user_by_username(session: AsyncSession, name: str) -> Optional[User]:
    stmt = select(User).where(User.username == name)
    result = await session.execute(stmt)
    return result.scalars().first()


async def get_all_users(session: AsyncSession) -> List[User]:
    stmt = select(User)
    result = await session.execute(stmt)
    return result.scalars().all()


async def search_users(session: AsyncSession, q: str, limit: int = 20) -> List[User]:
    stmt = (
        select(User)
        .where(User.username.ilike(f"%{q}%"))
        .limit(limit)
    )
    result = await session.execute(stmt)
    return result.scalars().all()


async def create_user(session: AsyncSession, data: UserCreate) -> User:
    user = User(
        username=data.username,
        email=data.email,
        password_hash=data.password  # или хэшируй, если хочешь
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def update_user(session: AsyncSession, user_id: int, data: UserUpdate) -> Optional[User]:
    user = await session.get(User, user_id)
    if not user:
        return None

    if data.username is not None:
        user.username = data.username
    if data.email is not None:
        user.email = data.email

    await session.commit()
    await session.refresh(user)
    return user


async def delete_user(session: AsyncSession, user_id: int) -> bool:
    user = await session.get(User, user_id)
    if not user:
        return False

    await session.delete(user)
    await session.commit()
    return True
