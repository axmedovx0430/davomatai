"""
Group model for organizing users (e.g., university groups, departments)
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# Many-to-many relationship table
user_groups = Table(
    'user_groups',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('group_id', Integer, ForeignKey('groups.id', ondelete='CASCADE'), primary_key=True),
    Column('joined_at', DateTime(timezone=True), server_default=func.now())
)


class Group(Base):
    __tablename__ = "groups"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    code = Column(String(50), unique=True, index=True)  # e.g., "CS-101", "MATH-201"
    description = Column(String(500))
    faculty = Column(String(255))  # Fakultet
    course = Column(Integer)  # Kurs (1, 2, 3, 4)
    semester = Column(Integer)  # Semestr (1, 2)
    academic_year = Column(String(20))  # O'quv yili (2024-2025)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    users = relationship("User", secondary=user_groups, back_populates="groups")
    schedules = relationship("Schedule", back_populates="group", cascade="all, delete-orphan")
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "description": self.description,
            "faculty": self.faculty,
            "course": self.course,
            "semester": self.semester,
            "academic_year": self.academic_year,
            "is_active": self.is_active,
            "student_count": len(self.users) if self.users else 0,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
    
    def to_dict_with_students(self):
        """Include student list"""
        data = self.to_dict()
        data["students"] = [
            {
                "id": user.id,
                "full_name": user.full_name,
                "employee_id": user.employee_id
            }
            for user in self.users
        ] if self.users else []
        return data
