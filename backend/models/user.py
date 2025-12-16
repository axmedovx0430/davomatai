"""
User model
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    employee_id = Column(String(50), unique=True, nullable=False, index=True)
    phone = Column(String(20))
    email = Column(String(255))
    role = Column(String(20), default="user")  # 'admin' or 'user'
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Telegram integration fields
    telegram_chat_id = Column(String(50), unique=True, nullable=True)
    telegram_username = Column(String(100), nullable=True)
    telegram_notifications = Column(Boolean, default=True)
    telegram_registered_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    faces = relationship("Face", back_populates="user", cascade="all, delete-orphan")
    attendance_records = relationship("Attendance", back_populates="user")
    api_keys = relationship("APIKey", back_populates="user")
    groups = relationship("Group", secondary="user_groups", back_populates="users")
    
    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "employee_id": self.employee_id,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "face_count": len(self.faces) if self.faces else 0,
            "groups": [{"id": g.id, "name": g.name, "code": g.code} for g in self.groups] if self.groups else [],
            "telegram_chat_id": self.telegram_chat_id,
            "telegram_username": self.telegram_username,
            "telegram_notifications": self.telegram_notifications,
            "telegram_registered_at": self.telegram_registered_at.isoformat() if self.telegram_registered_at else None
        }
