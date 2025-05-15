import os

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:20122001@localhost:5432/usermanagementdb")
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7 
    SECRET_KEY = os.getenv('SECRET_KEY', 'my-secret-key')
    ALGORITHM = "HS256"

settings = Settings()