"""
Time Settings Model
Admin-configurable time intervals for attendance system
"""
from sqlalchemy import Column, Integer, String, Time, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
from datetime import time as dt_time


class TimeSettings(Base):
    __tablename__ = "time_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    work_start_time = Column(Time, nullable=False, default=dt_time(9, 0))  # Default 09:00
    late_threshold_minutes = Column(Integer, nullable=False, default=30)  # Default 30 minutes
    duplicate_check_minutes = Column(Integer, nullable=False, default=120)  # Default 120 minutes (2 hours)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    
    # Relationship
    creator = relationship("User", foreign_keys=[created_by])
    
    def to_dict(self):
        return {
            "id": self.id,
            "work_start_time": self.work_start_time.strftime("%H:%M") if self.work_start_time else None,
            "late_threshold_minutes": self.late_threshold_minutes,
            "duplicate_check_minutes": self.duplicate_check_minutes,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
            "is_active": self.is_active
        }
