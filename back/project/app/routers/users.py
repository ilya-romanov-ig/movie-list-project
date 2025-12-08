# app/routers/users.py

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.crud.users import (
    get_user_by_id,
    get_user_by_username,
    get_all_users,
    search_users,
    create_user,
    update_user,
    delete_user
)
from app.schemas.user import UserCreate, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}")
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user


@router.get("")
async def list_users(
    q: str | None = Query(None, description="Search by username"),
    db: AsyncSession = Depends(get_db)
):
    if q:
        return await search_users(db, q)
    return await get_all_users(db)


@router.post("")
async def create_new_user(data: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, data)


@router.put("/{user_id}")
async def update_existing_user(
    user_id: int,
    data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    updated = await update_user(db, user_id, data)
    if not updated:
        raise HTTPException(404, "User not found")
    return updated


@router.delete("/{user_id}")
async def delete_existing_user(user_id: int, db: AsyncSession = Depends(get_db)):
    ok = await delete_user(db, user_id)
    if not ok:
        raise HTTPException(404, "User not found")
    return {"status": "deleted"}
