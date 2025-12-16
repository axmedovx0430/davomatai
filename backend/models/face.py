"""
Face model
"""
from sqlalchemy import Column, Integer, String, LargeBinary, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Face(Base):
    __tablename__ = "faces"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    embedding = Column(LargeBinary, nullable=False)  # numpy array as bytes
    image_path = Column(String(500))
    registered_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="faces")
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "image_path": self.image_path,
            "registered_at": self.registered_at.isoformat() if self.registered_at else None
        }
