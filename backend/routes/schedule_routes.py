"""
Schedule Routes - API endpoints for class schedule management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from services.schedule_service import schedule_service
from pydantic import BaseModel
from datetime import time, date
from typing import Optional, List

router = APIRouter(prefix="/api/schedules", tags=["schedules"])


# Pydantic schemas
class ScheduleCreate(BaseModel):
    name: str
    day_of_week: int  # 0=Monday, 6=Sunday
    start_time: str  # Format: "HH:MM"
    end_time: str  # Format: "HH:MM"
    group_id: Optional[int] = None
    late_threshold_minutes: Optional[int] = None
    duplicate_check_minutes: Optional[int] = None
    effective_from: Optional[str] = None  # Format: "YYYY-MM-DD"
    effective_to: Optional[str] = None    # Format: "YYYY-MM-DD"
    teacher: Optional[str] = None
    room: Optional[str] = None


class ScheduleUpdate(BaseModel):
    name: Optional[str] = None
    day_of_week: Optional[int] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    group_id: Optional[int] = None
    is_active: Optional[bool] = None
    late_threshold_minutes: Optional[int] = None
    duplicate_check_minutes: Optional[int] = None
    effective_from: Optional[str] = None
    effective_to: Optional[str] = None
    teacher: Optional[str] = None
    room: Optional[str] = None


from utils import parse_time

@router.post("", status_code=status.HTTP_201_CREATED)
def create_schedule(
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db)
):
    """Create a new class schedule"""
    try:
        # Parse time strings
        start_time_obj = parse_time(schedule_data.start_time)
        end_time_obj = parse_time(schedule_data.end_time)
        
        if not start_time_obj or not end_time_obj:
             raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid time format. Use HH:MM or HH:MM:SS"
            )

        
        # Validate day_of_week
        if schedule_data.day_of_week < 0 or schedule_data.day_of_week > 6:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="day_of_week must be between 0 (Monday) and 6 (Sunday)"
            )
        
        # Validate times
        if start_time_obj >= end_time_obj:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="start_time must be before end_time"
            )
        
        # Parse dates if provided
        effective_from_obj = None
        effective_to_obj = None
        
        if schedule_data.effective_from:
            effective_from_obj = date.fromisoformat(schedule_data.effective_from)
        if schedule_data.effective_to:
            effective_to_obj = date.fromisoformat(schedule_data.effective_to)

        schedule = schedule_service.create_schedule(
            db=db,
            name=schedule_data.name,
            day_of_week=schedule_data.day_of_week,
            start_time=start_time_obj,
            end_time=end_time_obj,
            group_id=schedule_data.group_id,
            late_threshold_minutes=schedule_data.late_threshold_minutes,
            duplicate_check_minutes=schedule_data.duplicate_check_minutes,
            effective_from=effective_from_obj,
            effective_to=effective_to_obj,
            teacher=schedule_data.teacher,
            room=schedule_data.room
        )
        
        return {
            "success": True,
            "message": "Schedule created successfully",
            "schedule": schedule.to_dict()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid time format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/week")
def get_week_schedules(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get all active schedules organized by weekday, optionally filtered by date range
    """
    try:
        # Parse dates if provided
        start_date_obj = None
        end_date_obj = None
        
        if start_date:
            start_date_obj = date.fromisoformat(start_date)
        if end_date:
            end_date_obj = date.fromisoformat(end_date)
            
        week_schedule = schedule_service.get_week_schedules(db, start_date_obj, end_date_obj)
        
        # Convert to dict format
        result = {}
        for day, schedules in week_schedule.items():
            result[str(day)] = [s.to_dict() for s in schedules]
        
        return {
            "success": True,
            "schedules": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{schedule_id}")
def get_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """Get specific schedule by ID"""
    schedule = schedule_service.get_schedule_by_id(db, schedule_id)
    
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return {
        "success": True,
        "schedule": schedule.to_dict()
    }


@router.get("/{schedule_id}/stats")
def get_schedule_stats(
    schedule_id: int,
    date: str,  # Format: "YYYY-MM-DD"
    db: Session = Depends(get_db)
):
    """Get attendance statistics for a specific class on a specific date"""
    try:
        from datetime import date as date_class
        target_date = date_class.fromisoformat(date)
        stats = schedule_service.get_schedule_stats(db, schedule_id, target_date)
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "date": date,
            "stats": stats
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/{schedule_id}/attendance")
def get_schedule_attendance(
    schedule_id: int,
    date: str,  # Format: "YYYY-MM-DD"
    db: Session = Depends(get_db)
):
    """Get all attendance records for a specific class on a specific date"""
    try:
        from datetime import date as date_class
        target_date = date_class.fromisoformat(date)
        attendance_records = schedule_service.get_attendance_by_schedule(
            db, schedule_id, target_date
        )
        
        return {
            "success": True,
            "schedule_id": schedule_id,
            "date": date,
            "attendance": [record.to_dict() for record in attendance_records]
        }
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.put("/{schedule_id}")
def update_schedule(
    schedule_id: int,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db)
):
    """Update existing schedule"""
    try:
        # Parse time strings if provided
        start_time_obj = None
        end_time_obj = None
        
        if schedule_data.start_time:
            start_time_obj = parse_time(schedule_data.start_time)
        if schedule_data.end_time:
            end_time_obj = parse_time(schedule_data.end_time)
        
        # Validate day_of_week if provided
        if schedule_data.day_of_week is not None:
            if schedule_data.day_of_week < 0 or schedule_data.day_of_week > 6:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="day_of_week must be between 0 (Monday) and 6 (Sunday)"
                )
        
        # Parse dates if provided
        effective_from_obj = None
        effective_to_obj = None
        
        if schedule_data.effective_from:
            effective_from_obj = date.fromisoformat(schedule_data.effective_from)
        if schedule_data.effective_to:
            effective_to_obj = date.fromisoformat(schedule_data.effective_to)
            
        schedule = schedule_service.update_schedule(
            db=db,
            schedule_id=schedule_id,
            name=schedule_data.name,
            day_of_week=schedule_data.day_of_week,
            start_time=start_time_obj,
            end_time=end_time_obj,
            group_id=schedule_data.group_id,
            is_active=schedule_data.is_active,
            late_threshold_minutes=schedule_data.late_threshold_minutes,
            duplicate_check_minutes=schedule_data.duplicate_check_minutes,
            effective_from=effective_from_obj,
            effective_to=effective_to_obj,
            teacher=schedule_data.teacher,
            room=schedule_data.room
        )
        
        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Schedule not found"
            )
        
        return {
            "success": True,
            "message": "Schedule updated successfully",
            "schedule": schedule.to_dict()
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid time format: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.delete("/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    """Delete schedule"""
    success = schedule_service.delete_schedule(db, schedule_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    return {
        "success": True,
        "message": "Schedule deleted successfully"
    }
