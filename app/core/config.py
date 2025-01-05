import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from the root .env file
load_dotenv()
print(os.getenv('ENV', 'dev'))
class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str

    class Config:
        # Dynamically load the correct config file based on the ENV variable
        env_file = f"./config/{os.getenv('ENV', 'dev')}.env"  # Default to dev.env

settings = Settings()
