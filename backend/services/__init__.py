"""
Services package
"""
from .face_recognition_service import face_recognition_service
from .attendance_service import attendance_service
from .telegram_service import telegram_service

__all__ = ["face_recognition_service", "attendance_service", "telegram_service"]
