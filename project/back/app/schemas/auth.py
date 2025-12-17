from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

model_cfg = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


