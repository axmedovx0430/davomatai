"""
Time Settings Routes
API endpoints for managing attendance time settings
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.time_settings import TimeSettings
from pydantic import BaseModel
from typing import Optional
from datetime import time
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/settings", tags=["Settings"])


class TimeSettingsCreate(BaseModel):
    work_start_time: str  # Format: "HH:MM"
    late_threshold_minutes: int
    duplicate_check_minutes: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "work_start_time": "09:00",
                "late_threshold_minutes": 30,
                "duplicate_check_minutes": 120
            }
        }


@router.get("/time")
async def get_current_time_settings(db: Session = Depends(get_db)):
    """Get current active time settings"""
    settings = db.query(TimeSettings).filter(
        TimeSettings.is_active == 1
    ).order_by(TimeSettings.created_at.desc()).first()
    
    if not settings:
        # Return default settings if none exist
        return {
            "success": True,
            "settings": {
                "id": None,
                "work_start_time": "09:00",
                "late_threshold_minutes": 30,
                "duplicate_check_minutes": 120,
                "created_at": None,
                "is_active": 1
            }
        }
    
    return {
        "success": True,
        "settings": settings.to_dict()
    }


@router.post("/time")
async def create_time_settings(
    settings_data: TimeSettingsCreate,
    db: Session = Depends(get_db)
):
    """Create new time settings (deactivates previous settings)"""
    try:
        # Parse time string to time object
        hour, minute = map(int, settings_data.work_start_time.split(':'))
        work_time = time(hour, minute)
        
        # Deactivate all previous settings
        db.query(TimeSettings).update({"is_active": 0})
        
        # Create new settings
        new_settings = TimeSettings(
            work_start_time=work_time,
            late_threshold_minutes=settings_data.late_threshold_minutes,
            duplicate_check_minutes=settings_data.duplicate_check_minutes,
            is_active=1
        )
        
        db.add(new_settings)
        db.commit()
        db.refresh(new_settings)
        
        logger.info(f"New time settings created: {new_settings.to_dict()}")
        
        return {
            "success": True,
            "message": "Vaqt sozlamalari muvaffaqiyatli saqlandi",
            "settings": new_settings.to_dict()
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Noto'g'ri vaqt formati. HH:MM formatida kiriting (masalan: 09:00)"
        )
    except Exception as e:
        logger.error(f"Error creating time settings: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Xatolik yuz berdi: {str(e)}"
        )


@router.get("/time/history")
async def get_time_settings_history(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get history of time settings changes"""
    settings_list = db.query(TimeSettings).order_by(
        TimeSettings.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return {
        "success": True,
        "count": len(settings_list),
        "history": [s.to_dict() for s in settings_list]
    }
