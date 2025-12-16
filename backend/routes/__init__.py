from .face_routes import router as face_router
from .user_routes import router as user_router
from .attendance_routes import router as attendance_router
from .device_routes import router as device_router
from .time_settings_routes import router as settings_router
from .schedule_routes import router as schedule_router

__all__ = ["face_router", "user_router", "attendance_router", "device_router", "settings_router", "schedule_router"]
