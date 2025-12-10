import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "GitHub AI Genius"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = "YOUR_SUPER_SECRET_KEY_CHANGE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # Database
    DATABASE_URL: str = "sqlite:///./github_ai_genius.db"
    
    # AI Defaults
    DEFAULT_MODEL_PROVIDER: str = "ollama"
    DEFAULT_MODEL_NAME: str = "llama3.2"
    
    # Paths
    WORKSPACE_DIR: str = os.path.join(os.getcwd(), "workspace")
    
    class Config:
        env_file = ".env"

settings = Settings()

# Ensure workspace exists
os.makedirs(settings.WORKSPACE_DIR, exist_ok=True)
