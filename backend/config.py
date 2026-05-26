import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # App
    APP_NAME = "ExamAce API"
    APP_VERSION = "1.0.0"
    DEBUG = os.getenv("DEBUG", "True") == "True"
    
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost/examace"
    )
    
    # JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    ALGORITHM = "HS256"
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # Redis
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS
    ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:8000",
        "https://examace.vercel.app",
    ]

settings = Settings()
