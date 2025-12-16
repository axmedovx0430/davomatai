"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    full_name: str = Field(..., min_length=1, max_length=255)
    employee_id: str = Field(..., min_length=1, max_length=50)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role: str = Field(default="user", pattern="^(admin|user)$")


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=1, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    role: Optional[str] = Field(None, pattern="^(admin|user)$")
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    face_count: int = 0

    class Config:
        from_attributes = True


class DeviceBase(BaseModel):
    device_name: str = Field(..., min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=255)


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(BaseModel):
    device_name: Optional[str] = Field(None, min_length=1, max_length=100)
    location: Optional[str] = Field(None, max_length=255)
    is_active: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    is_active: bool
    last_seen: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    user_name: str
    employee_id: str
    device_id: Optional[int]
    device_name: Optional[str]
    check_in_time: datetime
    confidence: float
    status: str

    class Config:
        from_attributes = True


class FaceResponse(BaseModel):
    id: int
    user_id: int
    image_path: Optional[str]
    registered_at: datetime

    class Config:
        from_attributes = True


class StatsResponse(BaseModel):
    total_users: int
    present: int
    late: int
    absent: int
    attendance_rate: float


class FaceRecognitionResponse(BaseModel):
    success: bool
    message: str
    recognized: bool
    user: Optional[UserResponse] = None
    confidence: Optional[float] = None
    attendance: Optional[AttendanceResponse] = None
    duplicate: bool = False
