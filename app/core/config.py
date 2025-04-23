import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "NeoBuild API"
    DESCRIPTION: str = "API for managing build and release processes"
    VERSION: str = "0.1.0"
    
    # Настройки CORS
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    model_config = {
        "case_sensitive": True
    }

settings = Settings() 