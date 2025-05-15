from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.helpers.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str

    model_config = {
        'from_attributes': True
    }

class UserItemResponse(UserBase):
    id: int
    is_active: bool
    role: str

class UserCreateRequest(UserBase):
    password: str
    role: UserRole = UserRole.USER
    is_active: bool = True  

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

class PaginationParams(BaseModel):
    skip: int = 0
    limit: int = 100

    model_config = {
        'extra': 'forbid'
    }

class PaginatedUserResponse(BaseModel):
    total: int
    skip: int
    limit: int
    data: List[UserItemResponse]