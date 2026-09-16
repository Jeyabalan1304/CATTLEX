from pydantic import BaseModel
from typing import Optional
import datetime

class UserBase(BaseModel):
    name: str
    email: str
    role: str = "FARMER"

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class LoginRequest(BaseModel):
    email: str
    password: str
