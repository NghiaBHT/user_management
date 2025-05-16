import pytest
from unittest.mock import patch, MagicMock, PropertyMock
from fastapi_sqlalchemy import db

from app.services.srv_user import UserService
from app.schemas.sche_user import UserCreateRequest, UserUpdateRequest
from app.models.model_user import User
from app.helpers.enums import UserRole
from app.core.security import get_password_hash # Imported to potentially spy or if its direct output is needed

def test_create_user_success():
    """Test successful user creation."""
    mock_db_instance = MagicMock()

    with patch.object(type(db), "session", new_callable=PropertyMock) as mock_session:
        mock_session.return_value = mock_db_instance
        mock_db_instance.query.return_value.filter.return_value.first.return_value = None

        with patch('app.services.srv_user.get_password_hash', return_value="fake_hashed_password"):
            user_data = UserCreateRequest(
                email="newuser@example.com",
                full_name="New User",
                password="password123",
                role=UserRole.USER,
                is_active=True
            )

            created_user = UserService.create_user(data=user_data)

            assert created_user is not None
            assert created_user.email == user_data.email
            assert created_user.full_name == user_data.full_name
            assert created_user.hashed_password == "fake_hashed_password"
            assert created_user.role == user_data.role.value
            assert created_user.is_active == user_data.is_active

            mock_db_instance.add.assert_called_once()
            mock_db_instance.commit.assert_called_once()