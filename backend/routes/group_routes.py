"""
Group Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from database import get_db
from models.group import Group
from models.user import User
from typing import List, Optional
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/groups", tags=["Groups"])


# Pydantic schemas
class GroupCreate(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[int] = None
    semester: Optional[int] = None
    academic_year: Optional[str] = None


class GroupUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    faculty: Optional[str] = None
    course: Optional[int] = None
    semester: Optional[int] = None
    academic_year: Optional[str] = None
    is_active: Optional[bool] = None


class AddStudentsRequest(BaseModel):
    user_ids: List[int]


@router.get("")
async def get_groups(
    skip: int = 0,
    limit: int = 100,
    faculty: Optional[str] = None,
    course: Optional[int] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db)
):
    """Get all groups with optional filters"""
    query = db.query(Group)
    
    if faculty:
        query = query.filter(Group.faculty == faculty)
    if course:
        query = query.filter(Group.course == course)
    if is_active is not None:
        query = query.filter(Group.is_active == is_active)
    
    groups = query.offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "count": len(groups),
        "groups": [group.to_dict() for group in groups]
    }


@router.get("/{group_id}")
async def get_group(group_id: int, db: Session = Depends(get_db)):
    """Get specific group with student list"""
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    return {
        "success": True,
        "group": group.to_dict_with_students()
    }


@router.post("")
async def create_group(group_data: GroupCreate, db: Session = Depends(get_db)):
    """Create new group"""
    # Check if code already exists
    existing = db.query(Group).filter(Group.code == group_data.code).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Group with code '{group_data.code}' already exists"
        )
    
    group = Group(**group_data.dict())
    db.add(group)
    db.commit()
    db.refresh(group)
    
    logger.info(f"Group created: {group.name} ({group.code})")
    
    return {
        "success": True,
        "message": "Group created successfully",
        "group": group.to_dict()
    }


@router.put("/{group_id}")
async def update_group(
    group_id: int,
    group_data: GroupUpdate,
    db: Session = Depends(get_db)
):
    """Update group information"""
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Update fields
    update_data = group_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(group, field, value)
    
    db.commit()
    db.refresh(group)
    
    return {
        "success": True,
        "message": "Group updated successfully",
        "group": group.to_dict()
    }


@router.delete("/{group_id}")
async def delete_group(group_id: int, db: Session = Depends(get_db)):
    """Delete group"""
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    db.delete(group)
    db.commit()
    
    return {
        "success": True,
        "message": "Group deleted successfully"
    }


@router.post("/{group_id}/students")
async def add_students_to_group(
    group_id: int,
    request: AddStudentsRequest,
    db: Session = Depends(get_db)
):
    """Add students to group"""
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Get users
    users = db.query(User).filter(User.id.in_(request.user_ids)).all()
    
    if len(users) != len(request.user_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Some users not found"
        )
    
    # Add users to group
    for user in users:
        if user not in group.users:
            group.users.append(user)
    
    db.commit()
    db.refresh(group)
    
    return {
        "success": True,
        "message": f"Added {len(users)} students to group",
        "group": group.to_dict_with_students()
    }


@router.delete("/{group_id}/students/{user_id}")
async def remove_student_from_group(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db)
):
    """Remove student from group"""
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    if user in group.users:
        group.users.remove(user)
        db.commit()
    
    return {
        "success": True,
        "message": "Student removed from group"
    }


@router.get("/{group_id}/attendance")
async def get_group_attendance(
    group_id: int,
    date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get attendance for all students in group"""
    from models.attendance import Attendance
    from datetime import datetime, date as date_type
    
    group = db.query(Group).filter(Group.id == group_id).first()
    
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )
    
    # Parse date
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    else:
        target_date = date_type.today()
    
    # Get attendance for all students in group
    attendance_records = []
    for user in group.users:
        records = db.query(Attendance).filter(
            Attendance.user_id == user.id,
            func.date(Attendance.check_in_time) == target_date
        ).all()
        
        attendance_records.append({
            "user": user.to_dict(),
            "attendance": [record.to_dict() for record in records] if records else []
        })
    
    return {
        "success": True,
        "group": group.to_dict(),
        "date": str(target_date),
        "attendance": attendance_records
    }
