import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# load the .env file from our directory
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Notes Summarizer"
    API_KEY: str = os.getenv('API_KEY', 'demo-key')
    JWT_SECRET_KEY: str = os.getenv('JWT_SECRET_KEY', 'secret')
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv('DATABASE_URL')
    SUMMARIZER_MODEL: str = os.getenv('SUMMARIZER_MODEL')
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    
settings = Settings()