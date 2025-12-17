# app/security/jwt.py
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db import async_session
from sqlalchemy import select
from app.models.user import User

from app.config import settings

SECRET_KEY = settings.JWT_SECRET
ALGORITHM = settings.JWT_ALG
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
optional_security = HTTPBearer(auto_error=False)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    # sub всегда строкой!
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(optional_security)
) -> Optional[User]:
    if credentials is None:
        return None
    
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        
        user_id = int(user_id)
        
    except (JWTError, ValueError):
        return None
    
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
    
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # приводим назад
        user_id = int(user_id)

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

