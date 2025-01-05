import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str

    class Config:
        env_file = f"./config/{os.getenv('ENV', 'dev')}.env"  # Default to dev.env

settings = Settings()
