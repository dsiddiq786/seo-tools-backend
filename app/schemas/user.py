from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True
