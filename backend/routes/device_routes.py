"""
Device Management Routes
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.device import Device
from middleware.auth_middleware import generate_api_key
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/devices", tags=["Devices"])


class DeviceCreate(BaseModel):
    device_name: str
    location: Optional[str] = None


class DeviceUpdate(BaseModel):
    device_name: Optional[str] = None
    location: Optional[str] = None
    is_active: Optional[bool] = None


@router.get("")
async def get_devices(
    is_active: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    """Get all devices"""
    query = db.query(Device)
    
    if is_active is not None:
        query = query.filter(Device.is_active == is_active)
    
    devices = query.all()
    
    return {
        "success": True,
        "count": len(devices),
        "devices": [device.to_dict() for device in devices]
    }


@router.get("/{device_id}")
async def get_device(device_id: int, db: Session = Depends(get_db)):
    """Get device by ID"""
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    return {
        "success": True,
        "device": device.to_dict()
    }


@router.post("")
async def create_device(device_data: DeviceCreate, db: Session = Depends(get_db)):
    """Create new device and generate API key"""
    # Generate unique API key
    api_key = generate_api_key()
    
    device = Device(
        device_name=device_data.device_name,
        location=device_data.location,
        api_key=api_key,
        last_seen=datetime.now()
    )
    
    db.add(device)
    db.commit()
    db.refresh(device)
    
    logger.info(f"Device created: {device.device_name}")
    
    return {
        "success": True,
        "message": "Device created successfully",
        "device": device.to_dict(),
        "api_key": api_key  # Return API key only once during creation
    }


@router.put("/{device_id}")
async def update_device(
    device_id: int,
    device_data: DeviceUpdate,
    db: Session = Depends(get_db)
):
    """Update device"""
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    if device_data.device_name is not None:
        device.device_name = device_data.device_name
    if device_data.location is not None:
        device.location = device_data.location
    if device_data.is_active is not None:
        device.is_active = device_data.is_active
    
    db.commit()
    db.refresh(device)
    
    logger.info(f"Device updated: {device.device_name}")
    
    return {
        "success": True,
        "message": "Device updated successfully",
        "device": device.to_dict()
    }


@router.delete("/{device_id}")
async def delete_device(device_id: int, db: Session = Depends(get_db)):
    """Delete device"""
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    db.delete(device)
    db.commit()
    
    logger.info(f"Device deleted: {device.device_name}")
    
    return {
        "success": True,
        "message": "Device deleted successfully"
    }


@router.post("/{device_id}/regenerate-key")
async def regenerate_api_key(device_id: int, db: Session = Depends(get_db)):
    """Regenerate API key for a device"""
    device = db.query(Device).filter(Device.id == device_id).first()
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Device not found"
        )
    
    # Generate new API key
    new_api_key = generate_api_key()
    device.api_key = new_api_key
    
    db.commit()
    db.refresh(device)
    
    logger.info(f"API key regenerated for device: {device.device_name}")
    
    return {
        "success": True,
        "message": "API key regenerated successfully",
        "device": device.to_dict(),
        "api_key": new_api_key
    }
