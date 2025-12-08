from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

model_cfg = ConfigDict(from_attributes=True)

class UserBase(BaseModel):
    model_config = model_cfg

    id: int
    username: str


class UserListItem(UserBase):
    bio: Optional[str] = None


class UserPublic(UserBase):
    bio: Optional[str] = None
    socials: Optional[str] = None
    is_private: bool = False


class UserPrivate(UserBase):
    email: EmailStr
    bio: Optional[str] = None
    socials: Optional[str] = None
    is_private: bool = False


class UserCreate(BaseModel):
    model_config = model_cfg

    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    socials: Optional[str] = None
    is_private: Optional[bool] = None
