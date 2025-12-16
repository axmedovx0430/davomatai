"""
Device model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Device(Base):
    __tablename__ = "devices"
    
    id = Column(Integer, primary_key=True, index=True)
    device_name = Column(String(100), nullable=False)
    api_key = Column(String(255), unique=True, nullable=False, index=True)
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    last_seen = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    attendance_records = relationship("Attendance", back_populates="device")
    
    def to_dict(self):
        return {
            "id": self.id,
            "device_name": self.device_name,
            "location": self.location,
            "is_active": self.is_active,
            "last_seen": self.last_seen.isoformat() if self.last_seen else None,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
