from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserItemResponse(UserBase):
    id: int
    is_active: bool
    role: str

class UserCreateRequest(UserBase):
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = True  

class UserUpdateRequest(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    is_active: bool = True
    role: UserRole