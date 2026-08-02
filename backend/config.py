import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "PDF to DXF Professional Converter"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # Base directory
    BASE_DIR: Path = Path(__file__).resolve().parent
    
    # Directories
    UPLOAD_DIR: Path = BASE_DIR / "uploads"
    OUTPUT_DIR: Path = BASE_DIR / "outputs"
    LOG_DIR: Path = BASE_DIR / "logs"
    
    # File limits
    MAX_FILE_SIZE_MB: int = 100
    ALLOWED_EXTENSIONS: set = {".pdf"}
    
    # CORS Settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "*"
    ]
    
    # Conversion Defaults
    DEFAULT_DXF_VERSION: str = "2018"
    DEFAULT_SNAP_TOLERANCE: float = 0.0001
    DEFAULT_REMOVE_DUPLICATES: bool = True
    DEFAULT_JOIN_SEGMENTS: bool = True
    DEFAULT_EXTRACT_TEXT: bool = True
    
    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

# Ensure directories exist
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
settings.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
settings.LOG_DIR.mkdir(parents=True, exist_ok=True)
