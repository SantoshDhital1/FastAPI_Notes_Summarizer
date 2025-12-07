import os
from dotenv import load_dotenv

# load the .env file from our directory
load_dotenv()

class Settings:
    PROJECT_NAME = 'FastAPI Notes Summarizer',
    API_KEY = os.getenv('API_KEY', 'demo-key'),
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'secret'),
    JWT_ALGORITHM = 'HS256',
    DATABASE_URL = os.getenv('DATABASE_URL')
    SUMMARIZER_MODEL = os.getenv('SUMMARIZER_MODEL')
    ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
settings = Settings()