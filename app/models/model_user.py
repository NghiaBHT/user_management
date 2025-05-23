from sqlalchemy import Column, String, Boolean, DateTime
from app.models.model_base import BareBaseModel


class User(BareBaseModel):
    __tablename__ = "users"
    
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String(255))
    is_active = Column(Boolean, default=True)
    role = Column(String, default='user')
    last_login = Column(DateTime)