from datetime import datetime
import re
from typing import Optional, List
from pydantic import BaseModel, EmailStr, field_validator

from app.helpers.enums import UserRole


class UserBase(BaseModel):
    email: EmailStr
    full_name: str

    @field_validator('full_name')
    @classmethod
    def capitalize_full_name(cls, v: str) -> str:
        return ' '.join(word.capitalize() for word in v.split())

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

    @field_validator('password')
    @classmethod
    def password_validation(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[UserRole] = None

    @field_validator('password')
    @classmethod
    def password_validation(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'\d', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

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