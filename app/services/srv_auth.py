from typing import Optional
from fastapi_sqlalchemy import db

from app.core.security import verify_password
from app.models.model_user import User


class AuthService(object):
    __instance = None
    def __init__(self) -> None:
        pass

    @staticmethod
    def authenticate(*, email: str, password: str) -> Optional[User]:
        """
        Check username and password is correct.
        Return object User if correct, else return None
        """
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user