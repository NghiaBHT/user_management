from typing import Any
from fastapi import APIRouter, Depends, Query, HTTPException

from app.helpers.enums import UserRole
from app.schemas.sche_base import CustomException, DataResponse
from app.schemas.sche_user import (
    UserCreateRequest,
    UserItemResponse,
    UserUpdateRequest,
    PaginatedUserResponse,
    PaginationParams
)
from app.services.srv_user import UserService
from app.core.dependencies import get_current_user, require_role
from app.models.model_user import User


router = APIRouter(prefix="/users", tags=["users"], dependencies=[Depends(require_role([UserRole.ADMIN]))])
@router.post("", response_model=DataResponse[UserItemResponse])
def create(user_data: UserCreateRequest, user_service: UserService = Depends()) -> Any:
    """
    API Create User
    """
    try:
        new_user = user_service.create_user(user_data)
        return DataResponse().success_response(data=new_user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise CustomException(http_code=500, code='500', message=f"An unexpected error occurred: {str(e)}")
    
@router.get("/{user_id}", response_model=DataResponse[UserItemResponse], dependencies=[Depends(require_role([UserRole.ADMIN]))])
def detail(user_id: int, user_service: UserService = Depends()) -> Any:
    """
    API get Detail User
    """
    try:
        user = user_service.get(user_id)
        return DataResponse().success_response(data=user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise CustomException(http_code=500, code='500', message=f"An unexpected error occurred: {str(e)}")
    
@router.put("/{user_id}", response_model=DataResponse[UserItemResponse], dependencies=[Depends(require_role([UserRole.ADMIN]))])
def update(user_id: int, user_data: UserUpdateRequest, user_service: UserService = Depends()) -> Any:
    """
    API update User
    """
    try:
        updated_user = user_service.update(user_id=user_id, data=user_data)
        return DataResponse().success_response(data=updated_user)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise CustomException(http_code=500, code='500', message=f"An unexpected error occurred: {str(e)}")

@router.delete("/{user_id}", response_model=DataResponse[UserItemResponse], dependencies=[Depends(require_role([UserRole.ADMIN]))])
def delete(user_id: int, user_service: UserService = Depends()) -> Any:
    """
    API delete User
    """
    try:
        user_deleted = user_service.delete(user_id=user_id)
        return DataResponse().success_response(data=user_deleted)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise CustomException(http_code=500, code='500', message=f"An unexpected error occurred: {str(e)}")

@router.get("/", response_model=DataResponse[PaginatedUserResponse], dependencies=[Depends(require_role([UserRole.ADMIN]))])
def list_all_users(
    skip: int = Query(0, ge=0, description="Number of items to skip"), 
    limit: int = Query(100, ge=1, le=200, description="Number of items to return per page"),
    user_service: UserService = Depends()
) -> Any:
    """
    API List Users (Admin only)
    Retrieves a paginated list of users. Requires admin privileges.
    """
    try:
        users, total_count = user_service.list_users(skip=skip, limit=limit)
        paginated_data = PaginatedUserResponse(
            total=total_count,
            skip=skip,
            limit=limit,
            data=[UserItemResponse.model_validate(user) for user in users]
        )
        return DataResponse().success_response(data=paginated_data)
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise CustomException(http_code=500, code='500', message=f"An error occurred: {str(e)}")
