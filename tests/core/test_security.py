import pytest
import jwt
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException
from starlette import status

from app.core.security import verify_token, create_access_token
from app.core.config import settings

# Test user ID for generating tokens
TEST_USER_ID = 1


def test_verify_token_valid():
    """Test verify_token with a valid token."""
    #Action
    token = create_access_token(user_id=TEST_USER_ID)
    user_id = verify_token(token)

    #Assert 
    assert user_id == str(TEST_USER_ID)


def test_verify_token_invalid_signature():
    """Test verify_token with a token signed with a wrong secret key."""
    #Arrange
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
        "user_id": str(TEST_USER_ID)
    }
    invalid_token = jwt.encode(payload, "WRONG_SECRET_KEY", algorithm=settings.ALGORITHM)
    
    #Action
    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token)

    #Assert 
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_verify_token_expired():
    """Test verify_token with an expired token."""
    # Create a token that expired 1 second ago
    #Arrange
    expired_token = create_access_token(user_id=TEST_USER_ID, expires_delta=timedelta(seconds=-1))
    
    #Action
    with pytest.raises(HTTPException) as exc_info:
        verify_token(expired_token)

    #Assert 
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_verify_token_missing_user_id():
    """Test verify_token with a token payload missing the 'user_id' field."""
    #Arrange
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
    }
    token_missing_userid = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    #Action
    with pytest.raises(HTTPException) as exc_info:
        verify_token(token_missing_userid)

    #Assert 
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"


def test_verify_token_malformed():
    """Test verify_token with a malformed token string."""
    #Arrange
    malformed_token = "this.is.not.a.valid.jwt"

    #Action
    with pytest.raises(HTTPException) as exc_info:
        verify_token(malformed_token)

    #Assert 
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
    assert exc_info.value.detail == "Could not validate credentials"
