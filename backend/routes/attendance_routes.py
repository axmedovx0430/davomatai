"""
Attendance Routes
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.attendance import Attendance
from models.user import User
from services.attendance_service import attendance_service
from datetime import datetime, timedelta
from utils import get_current_time, get_today_range
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/attendance", tags=["Attendance"])


@router.get("/health")
async def attendance_health():
    """Health check for attendance router"""
    return {"status": "ok", "router": "attendance"}


@router.get("")
async def get_attendance(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    user_id: Optional[int] = None,
    group_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get attendance records with optional filtering
    
    Args:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        user_id: Filter by user ID
        group_id: Filter by group ID
        skip: Pagination offset
        limit: Pagination limit
    """
    # Default to last 30 days if no dates provided
    if not start_date:
        start_dt = get_current_time() - timedelta(days=30)
    else:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    
    if not end_date:
        end_dt = get_current_time() + timedelta(days=1)
    else:
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    records = attendance_service.get_attendance_by_date_range(
        db=db,
        start_date=start_dt,
        end_date=end_dt,
        user_id=user_id,
        group_id=group_id
    )
    
    # Apply pagination
    total = len(records)
    records = records[skip:skip + limit]
    
    return {
        "success": True,
        "total": total,
        "count": len(records),
        "attendance": [record.to_dict() for record in records]
    }


@router.get("/today")
async def get_today_attendance(db: Session = Depends(get_db)):
    """Get today's attendance records"""
    records = attendance_service.get_today_attendance(db)
    
    return {
        "success": True,
        "date": get_current_time().strftime("%Y-%m-%d"),
        "count": len(records),
        "attendance": [record.to_dict() for record in records]
    }


@router.get("/stats")
async def get_attendance_stats(db: Session = Depends(get_db)):
    """Get today's attendance statistics"""
    from models.schedule import Schedule
    from models.group import Group
    from sqlalchemy import and_, or_
    
    records = attendance_service.get_today_attendance(db)
    
    # Get today's day of week (0=Monday, 6=Sunday)
    today = get_current_time()
    day_of_week = today.weekday()
    current_date = today.date()
    
    # Get all active schedules for today
    active_schedules = db.query(Schedule).filter(
        and_(
            Schedule.is_active == True,
            Schedule.day_of_week == day_of_week,
            or_(Schedule.effective_from.is_(None), Schedule.effective_from <= current_date),
            or_(Schedule.effective_to.is_(None), Schedule.effective_to >= current_date)
        )
    ).all()
    
    # Count unique users who should attend today (based on their groups)
    users_with_schedules = set()
    for schedule in active_schedules:
        if schedule.group_id:
            # Get users in this group
            group_users = db.query(User).join(
                User.groups
            ).filter(
                Group.id == schedule.group_id,
                User.is_active == True
            ).all()
            users_with_schedules.update([u.id for u in group_users])
        else:
            # If no group (public schedule), we DO NOT include all users in "Expected" count
            # to avoid inflating the "Absent" count.
            # Only users who actually attend will be counted in "Present"/"Late"
            pass
    
    total_users = len(users_with_schedules)
    
    # Calculate stats based on UNIQUE users
    present_users = set()
    late_users = set()
    
    # Group records by user
    user_records = {}
    for r in records:
        if r.user_id not in user_records:
            user_records[r.user_id] = []
        user_records[r.user_id].append(r)
        
    for user_id, u_records in user_records.items():
        # If user has ANY late record, mark as late (strict)
        # OR: If user has ANY present record, mark as present?
        # Let's go with: If user is late to ANY class, they are "Late" for the day
        is_late = any(r.status == 'late' for r in u_records)
        
        if is_late:
            late_users.add(user_id)
        else:
            present_users.add(user_id)
            
    # If a user attended but was not in "users_with_schedules" (e.g. public schedule),
    # we should probably add them to total_users so percentages make sense?
    # Or just keep total_users as "Expected" users.
    # Let's add unexpected attendees to total_users to avoid > 100% attendance
    unexpected_attendees = (present_users | late_users) - users_with_schedules
    total_users += len(unexpected_attendees)
    
    present_count = len(present_users)
    late_count = len(late_users)
    absent_count = total_users - (present_count + late_count)
    
    # Ensure absent count is not negative
    if absent_count < 0:
        absent_count = 0
    
    return {
        "success": True,
        "date": today.strftime("%Y-%m-%d"),
        "stats": {
            "total_users": total_users,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "attendance_rate": round(((present_count + late_count) / total_users * 100), 2) if total_users > 0 else 0
        }
    }


@router.get("/user/{user_id}/stats")
async def get_user_stats(
    user_id: int,
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get attendance statistics for a specific user"""
    stats = attendance_service.get_user_attendance_stats(db, user_id, days)
    
    return {
        "success": True,
        "user_id": user_id,
        "period_days": days,
        "stats": stats
    }


@router.get("/user/{user_id}")
async def get_user_attendance(
    user_id: int,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get attendance records for a specific user"""
    # Default to last 30 days
    if not start_date:
        start_dt = get_current_time() - timedelta(days=30)
    else:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")
    
    if not end_date:
        end_dt = get_current_time() + timedelta(days=1)
    else:
        end_dt = datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=1)
    
    records = attendance_service.get_attendance_by_date_range(
        db=db,
        start_date=start_dt,
        end_date=end_dt,
        user_id=user_id
    )
    
    return {
        "success": True,
        "user_id": user_id,
        "count": len(records),
        "attendance": [record.to_dict() for record in records]
    }

