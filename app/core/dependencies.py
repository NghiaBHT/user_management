from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
from fastapi_sqlalchemy import db

from app.core.security import verify_token
from app.models.model_user import User
from app.helpers.enums import UserRole

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    user_id_str = verify_token(credentials.credentials)
    
    try:
        user_id = int(user_id_str)
    except ValueError:
        # This case should ideally be caught by verify_token if user_id is not a valid format
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_user = db.session.query(User).get(user_id)

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, # Or 401, depending on desired behavior
            detail="Inactive user"
        )
        
    return current_user


def require_role(required_roles: list[UserRole]):
    def role_checker(current_user: User = Depends(get_current_user)):
        if current_user.role not in [role.value for role in required_roles]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied"
            )
        return current_user
    return role_checker