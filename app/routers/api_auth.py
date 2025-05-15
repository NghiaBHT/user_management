from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from fastapi_sqlalchemy import db
from pydantic import BaseModel, EmailStr

from app.core.dependencies import get_current_user
from app.core.security import create_access_token
from app.models.model_user import User
from app.schemas.sche_base import DataResponse
from app.schemas.sche_user import UserItemResponse
from app.services.srv_auth import AuthService
from app.schemas.sche_token import Token


router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    username: EmailStr
    password: str


@router.post('/', response_model=DataResponse[Token])
def login_access_token(form_data: LoginRequest, user_service: AuthService = Depends()):
    user = user_service.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect email or password')
    elif not user.is_active:
        raise HTTPException(status_code=401, detail='Inactive user')

    user.last_login = datetime.now()
    db.session.commit()

    return DataResponse().success_response({
        'access_token': create_access_token(user_id=user.id)
    })

@router.get("/me", response_model=DataResponse[UserItemResponse])
def read_current_user(current_user: User = Depends(get_current_user)) -> Any:
    """
    API Get Current User Information
    """
    return DataResponse().success_response(data=current_user)

