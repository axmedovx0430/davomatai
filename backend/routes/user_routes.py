"""
User Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/users", tags=["Users"])


class UserCreate(BaseModel):
    full_name: str
    employee_id: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: str = "user"

    @field_validator('email', 'phone', mode='before')
    @classmethod
    def empty_string_to_none(cls, v):
        if v == "":
            return None
        return v


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("")
async def get_users(
    skip: int = 0,
    limit: int = 100,
    is_active: Optional[bool] = None,
    group_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all users with optional filtering"""
    query = db.query(User)
    
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    
    if group_id:
        from models.group import Group
        query = query.join(User.groups).filter(Group.id == group_id)
    
    users = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "count": len(users),
        "users": [user.to_dict() for user in users]
    }


@router.get("/{user_id}")
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get user by ID"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "success": True,
        "user": user.to_dict()
    }


@router.get("/employee/{employee_id}")
async def get_user_by_employee_id(employee_id: str, db: Session = Depends(get_db)):
    """Get user by employee ID"""
    user = db.query(User).filter(User.employee_id == employee_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "success": True,
        "user": user.to_dict()
    }



@router.get("/telegram/{telegram_id}")
async def get_user_by_telegram_id(telegram_id: str, db: Session = Depends(get_db)):
    """Get user by Telegram ID"""
    user = db.query(User).filter(User.telegram_chat_id == telegram_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {
        "success": True,
        "user": user.to_dict()
    }


@router.post("")
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Create new user"""
    # Check if employee_id already exists
    existing = db.query(User).filter(User.employee_id == user_data.employee_id).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID already exists"
        )
    
    user = User(
        full_name=user_data.full_name,
        employee_id=user_data.employee_id,
        phone=user_data.phone,
        email=user_data.email,
        role=user_data.role
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    logger.info(f"User created: {user.employee_id}")
    
    return {
        "success": True,
        "message": "User created successfully",
        "user": user.to_dict()
    }


@router.put("/{user_id}")
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update fields
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.phone is not None:
        user.phone = user_data.phone
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.role is not None:
        user.role = user_data.role
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    db.commit()
    db.refresh(user)
    
    logger.info(f"User updated: {user.employee_id}")
    
    return {
        "success": True,
        "message": "User updated successfully",
        "user": user.to_dict()
    }


@router.delete("/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user (soft delete by setting is_active=False)"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Soft delete
    user.is_active = False
    db.commit()
    
    logger.info(f"User deleted: {user.employee_id}")
    
    return {
        "success": True,
        "message": "User deleted successfully"
    }
