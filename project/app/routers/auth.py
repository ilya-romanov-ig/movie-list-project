# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select

from app.security.hash import verify_password, get_password_hash
from app.security.jwt import create_access_token, get_current_user
from app.db import async_session
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Auth"])


# -------------------
# REGISTRATION
# -------------------
@router.post("/register")
async def register(username: str, email: str, password: str):
    async with async_session() as session:
        exists = await session.scalar(select(User).where(User.email == email))
        if exists:
            raise HTTPException(400, "User already exists")

        new_user = User(
            username=username,
            email=email,
            password_hash=get_password_hash(password),
            socials={}
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        return {"msg": "OK", "id": new_user.id}


# -------------------
# LOGIN
# -------------------
from fastapi.security import OAuth2PasswordRequestForm

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.email == form.username))

    if not user or not verify_password(form.password, user.password_hash):
        raise HTTPException(401, "Invalid email or password")

    token = create_access_token({"sub": user.id})
    return {"access_token": token, "token_type": "bearer"}


# -------------------
# CURRENT USER
# -------------------
@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
