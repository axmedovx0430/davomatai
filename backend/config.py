"""
Configuration settings for the application
"""
from pydantic_settings import BaseSettings
from typing import List, Optional
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./attendance.db"
    
    # Security
    SECRET_KEY: str = "insecure-default-key"
    API_KEY_SALT: str = "default-salt"
    DEFAULT_DEVICE_API_KEY: str = ""
    DEFAULT_ADMIN_PASSWORD: str = "admin123"
    
    # Telegram
    TELEGRAM_BOT_TOKEN: str = ""
    TELEGRAM_PROXY_URL: Optional[str] = None
    TELEGRAM_API_BASE_URL: str = "https://api.telegram.org/bot"
    TELEGRAM_ADMIN_CHAT_IDS: str = ""
    
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
    FRONTEND_URL: str = "http://localhost:3000"
    
    # Hugging Face / Webhook
    SPACE_ID: Optional[str] = None
    WEBHOOK_URL: Optional[str] = None
    
    @property
    def frontend_url(self) -> str:
        """Get the public frontend URL, auto-detecting Hugging Face if needed"""
        # Prioritize SPACE_ID to get the public .hf.space URL
        if self.SPACE_ID:
            # username/space-name -> username-space-name.hf.space
            host = self.SPACE_ID.replace("/", "-").lower()
            return f"https://{host}.hf.space"
        
        # Fallback to FRONTEND_URL if it's not localhost
        if self.FRONTEND_URL and "localhost" not in self.FRONTEND_URL:
            return self.FRONTEND_URL
            
        return self.FRONTEND_URL

    @property
    def telegram_webhook_url(self) -> Optional[str]:
        """Construct webhook URL from SPACE_ID if not explicitly set"""
        if self.WEBHOOK_URL:
            return self.WEBHOOK_URL
        if self.SPACE_ID or (self.FRONTEND_URL and "localhost" not in self.FRONTEND_URL):
            return f"{self.frontend_url}/api/telegram/webhook"
        return None
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"
    
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
logger.info(f"DEBUG: Settings initialized. Frontend URL: {settings.frontend_url}")
logger.info(f"DEBUG: Webhook URL: {settings.telegram_webhook_url}")

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "faces"), exist_ok=True)
os.makedirs(os.path.join(settings.UPLOAD_DIR, "attendance"), exist_ok=True)