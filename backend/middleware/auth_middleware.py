"""
Authentication Middleware
"""
from fastapi import Request, HTTPException, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from database import SessionLocal
from models.device import Device
from models.api_key import APIKey
import hashlib
from config import settings
from typing import Optional

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def hash_api_key(api_key: str) -> str:
    """Hash API key for storage"""
    return hashlib.sha256(f"{api_key}{settings.API_KEY_SALT}".encode()).hexdigest()


async def verify_device_api_key(request: Request, api_key: str = None, db: Session = None) -> Optional[Device]:
    """
    Verify device API key
    
    Args:
        request: FastAPI request
        api_key: API key from header
        db: Optional database session
        
    Returns:
        Device object if valid, raises HTTPException otherwise
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    # Use provided session or create new one
    should_close = False
    if db is None:
        db = SessionLocal()
        should_close = True
    
    try:
        # Find device by API key
        device = db.query(Device).filter(
            Device.api_key == api_key,
            Device.is_active == True
        ).first()
        
        if not device:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Update last seen
        from datetime import datetime
        device.last_seen = datetime.now()
        db.commit()
        
        return device
    finally:
        if should_close:
            db.close()


async def verify_user_api_key(request: Request, api_key: str = None) -> Optional[int]:
    """
    Verify user API key
    
    Args:
        request: FastAPI request
        api_key: API key from header
        
    Returns:
        User ID if valid, raises HTTPException otherwise
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key required"
        )
    
    db: Session = SessionLocal()
    try:
        # Hash the provided key
        key_hash = hash_api_key(api_key)
        
        # Find API key
        api_key_obj = db.query(APIKey).filter(
            APIKey.key_hash == key_hash
        ).first()
        
        if not api_key_obj:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key"
            )
        
        # Check expiration
        if api_key_obj.expires_at:
            from datetime import datetime
            if datetime.now() > api_key_obj.expires_at:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="API key expired"
                )
        
        return api_key_obj.user_id
    finally:
        db.close()


def generate_api_key() -> str:
    """Generate random API key"""
    import secrets
    return secrets.token_urlsafe(32)
