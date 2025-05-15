from fastapi import HTTPException
from fastapi_sqlalchemy import db
from app.core.security import get_password_hash, verify_password
from app.models.model_user import User
from app.schemas.sche_user import UserCreateRequest, UserUpdateRequest
from typing import List, Tuple


class UserService(object):
    __instance = None
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_user(data: UserCreateRequest):
        exist_user = db.session.query(User).filter(User.email == data.email).first()
        if exist_user:
            raise HTTPException(status_code=409, detail='Email already exists')
        
        new_user = User(
            full_name=data.full_name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
            is_active=data.is_active,
            role=data.role.value,
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user
    
    @staticmethod
    def get(user_id: int) -> User:
        exist_user = db.session.query(User).get(user_id)
        if exist_user is None:
            raise HTTPException(status_code=404, detail='User not found')
        return exist_user
    
    @staticmethod
    def list_users(skip: int, limit: int) -> Tuple[List[User], int]:
        """List users with pagination."""
        query = db.session.query(User)
        total_count = query.count() # Get total count before pagination
        users = query.offset(skip).limit(limit).all()
        return users, total_count

    @staticmethod
    def update(user_id: int, data: UserUpdateRequest) -> User:
        user = db.session.query(User).get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')
        
        update_data = data.model_dump(exclude_unset=True)

        if 'email' in update_data and update_data['email'] != user.email:
            # Check if the new email already exists for another user
            existing_email_user = db.session.query(User).filter(User.email == update_data['email'], User.id != user_id).first()
            if existing_email_user:
                raise HTTPException(status_code=409, detail='Email already in use by another account')
        
        for field, value in update_data.items():
            if field == "password" and value is not None:
                setattr(user, "hashed_password", get_password_hash(value))
            elif field == "role" and value is not None:
                setattr(user, field, value.value) # Use enum value
            elif value is not None:
                setattr(user, field, value)
        
        db.session.commit()
        db.session.refresh(user) # Refresh to get updated state from DB if needed
        return user

    @staticmethod
    def delete(user_id: int):
        user = db.session.query(User).get(user_id)
        if user is None:
            raise HTTPException(status_code=404, detail='User not found')

        db.session.delete(user)
        db.session.commit()
        return user
    
    