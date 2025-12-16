"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str
    API_KEY_SALT: str
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str
    TELEGRAM_ADMIN_CHAT_IDS: str
    
    # InsightFace
    INSIGHTFACE_MODEL: str = "buffalo_s"  # Changed from buffalo_l to buffalo_s (smaller, less memory)
    FACE_MATCH_THRESHOLD: float = 0.4  # 0.5 o'rniga 0.4 (osonroq tanish)
    FACE_DETECTION_THRESHOLD: float = 0.6
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8080
    DEBUG: bool = False
    
    # CORS
    ALLOWED_ORIGINS: str = "*"
    
    # Attendance
    LATE_THRESHOLD_MINUTES: int = 30
    WORK_START_TIME: str = "09:00"
    
    # Frontend
    FRONTEND_URL: str = "https://0bdcea5eac151a5f13d25d52a69344c5.serveousercontent.com"  # Serveo URL
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
    @property
    def admin_chat_ids(self) -> List[int]:
        """Parse comma-separated chat IDs"""
        return [int(id.strip()) for id in self.TELEGRAM_ADMIN_CHAT_IDS.split(",") if id.strip()]
    
    @property
    def cors_origins(self) -> List[str]:
        """Parse comma-separated origins"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "faces"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "attendance"), exist_ok=True)
