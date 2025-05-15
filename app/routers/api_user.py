from typing import Any
from fastapi import APIRouter, Depends

from app.schemas.sche_base import CustomException, DataResponse
from app.schemas.sche_user import UserCreateRequest, UserItemResponse, UserUpdateRequest
from app.services.srv_user import UserService


router = APIRouter(prefix="/users", tags=["users"])
@router.post("", response_model=DataResponse[UserItemResponse])
def create(user_data: UserCreateRequest, user_service: UserService = Depends()) -> Any:
    """
    API Create User
    """
    try:
        new_user = user_service.create_user(user_data)
        return DataResponse().success_response(data=new_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
    
@router.get("/{user_id}", response_model=DataResponse[UserItemResponse])
def detail(user_id: int, user_service: UserService = Depends()) -> Any:
    """
    API get Detail User
    """
    try:
        return DataResponse().success_response(data=user_service.get(user_id))
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
    
@router.put("/{user_id}", response_model=DataResponse[UserItemResponse])
def update(user_id: int, user_data: UserUpdateRequest, user_service: UserService = Depends()) -> Any:
    """
    API update User
    """
    try:
        updated_user = user_service.update(user_id=user_id, data=user_data)
        return DataResponse().success_response(data=updated_user)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))