"""
Schedule Model - Class/Lesson Schedule
"""
from sqlalchemy import Column, Integer, String, Time, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class Schedule(Base):
    """
    Schedule model for storing class/lesson schedules
    """
    __tablename__ = "schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)  # Class/Subject name (e.g., "Matematika")
    day_of_week = Column(Integer, nullable=False)  # 0=Monday, 6=Sunday
    start_time = Column(Time, nullable=False)  # Class start time
    end_time = Column(Time, nullable=False)  # Class end time
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="CASCADE"), nullable=True)  # Optional group link
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Schedule-specific settings (overrides global settings)
    late_threshold_minutes = Column(Integer, nullable=True)
    duplicate_check_minutes = Column(Integer, nullable=True)

    # Effective dates for weekly filtering
    effective_from = Column(DateTime, nullable=True)  # Start date of the schedule
    effective_to = Column(DateTime, nullable=True)    # End date of the schedule
    
    # Additional details
    teacher = Column(String(100), nullable=True)
    room = Column(String(50), nullable=True)
    
    # Relationships
    group = relationship("Group", back_populates="schedules")
    attendance_records = relationship("Attendance", back_populates="schedule", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Schedule {self.name} - Day {self.day_of_week} {self.start_time}-{self.end_time}>"
    
    def to_dict(self):
        """Convert schedule to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "day_of_week": self.day_of_week,
            "start_time": self.start_time.strftime("%H:%M") if self.start_time else None,
            "end_time": self.end_time.strftime("%H:%M") if self.end_time else None,
            "group_id": self.group_id,
            "is_active": self.is_active,
            "late_threshold_minutes": self.late_threshold_minutes,
            "duplicate_check_minutes": self.duplicate_check_minutes,
            "effective_from": self.effective_from.isoformat() if self.effective_from else None,
            "effective_to": self.effective_to.isoformat() if self.effective_to else None,
            "teacher": self.teacher,
            "room": self.room,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
