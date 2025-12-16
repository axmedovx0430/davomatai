"""
Attendance model
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Attendance(Base):
    __tablename__ = "attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    device_id = Column(Integer, ForeignKey("devices.id"))
    schedule_id = Column(Integer, ForeignKey("schedules.id", ondelete="CASCADE"), nullable=True)  # Link to class schedule
    check_in_time = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    confidence = Column(Float)
    image_path = Column(String(500))
    status = Column(String(20), default="present")  # 'present', 'late', 'absent'
    
    # Detection tracking
    detection_count = Column(Integer, default=1)  # Necha marta ko'rildi
    last_seen_time = Column(DateTime(timezone=True), server_default=func.now())  # Oxirgi ko'rilgan vaqt
    
    # Relationships
    user = relationship("User", back_populates="attendance_records")
    device = relationship("Device", back_populates="attendance_records")
    schedule = relationship("Schedule", back_populates="attendance_records")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "user_name": self.user.full_name if self.user else None,
            "employee_id": self.user.employee_id if self.user else None,
            "device_id": self.device_id,
            "device_name": self.device.device_name if self.device else None,
            "schedule_id": self.schedule_id,
            "schedule_name": self.schedule.name if self.schedule else None,
            "check_in_time": self.check_in_time.isoformat() if self.check_in_time else None,
            "confidence": self.confidence,
            "image_path": self.image_path,
            "status": self.status,
            "detection_count": self.detection_count,
            "last_seen_time": self.last_seen_time.isoformat() if self.last_seen_time else None
        }
