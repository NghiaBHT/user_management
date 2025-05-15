import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", " ")
    ACCESS_TOKEN_EXPIRE_SECONDS: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS", 60 * 60 * 24 * 7))
    SECRET_KEY: str = os.getenv('SECRET_KEY', '')
    ALGORITHM: str = os.getenv('ALGORITHM', "")

settings = Settings()