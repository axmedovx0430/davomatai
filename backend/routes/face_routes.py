"""
Face Recognition Routes
"""
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status, Header
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.face import Face
from models.device import Device
from services.face_recognition_service import face_recognition_service
from services.attendance_service import attendance_service
from services.telegram_service import telegram_service
from middleware.auth_middleware import verify_device_api_key
import cv2
import numpy as np
from datetime import datetime
import os
from config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/face", tags=["Face Recognition"])


@router.post("/upload")
async def upload_face_for_recognition(
    file: UploadFile = File(...),
    x_api_key: str = Header(..., alias="X-API-Key"),
    db: Session = Depends(get_db)
):
    """
    ESP32-CAM endpoint: Upload face image for recognition
    
    Args:
        file: Image file (400x400 cropped face)
        x_api_key: Device API key
        db: Database session
        
    Returns:
        Recognition result with user info
    """
    logger.info(f"ESP32 REQUEST RECEIVED - File: {file.filename}, Size: {file.size if hasattr(file, 'size') else 'unknown'}")
    
    # Verify device API key
    device = await verify_device_api_key(None, x_api_key, db)
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file"
            )
        
        # Extract embedding from uploaded image
        query_embedding = face_recognition_service.get_embedding(image)
        
        if query_embedding is None:
            logger.warning("No face detected in uploaded image")
            return {
                "success": False,
                "message": "No face detected in image",
                "recognized": False
            }
        
        logger.info("Face detected in image, searching database...")
        
        # Get all face embeddings from database
        faces = db.query(Face).join(User).filter(User.is_active == True).all()
        
        if not faces:
            logger.warning("No registered faces in database")
            return {
                "success": False,
                "message": "No registered faces in database",
                "recognized": False
            }
        
        # Convert database embeddings
        database_embeddings = []
        for face in faces:
            db_embedding = face_recognition_service.bytes_to_embedding(face.embedding)
            database_embeddings.append((face.id, db_embedding))
        
        # Find best match
        match_result = face_recognition_service.find_best_match(query_embedding, database_embeddings)
        
        if match_result is None:
            logger.info("Face not recognized (no match found)")
            return {
                "success": True,
                "message": "Face detected but not recognized",
                "recognized": False
            }
        
        face_id, confidence = match_result
        logger.info(f"Face recognized! Face ID: {face_id}, Confidence: {confidence}")
        
        # Get user info
        matched_face = db.query(Face).filter(Face.id == face_id).first()
        user = matched_face.user
        
        # Check for duplicate attendance today
        if attendance_service.check_duplicate_today(db, user.id):
            logger.info(f"Duplicate attendance for user {user.full_name}")
            return {
                "success": True,
                "message": f"User {user.full_name} already checked in today",
                "recognized": True,
                "user": user.to_dict(),
                "confidence": round(confidence * 100, 2),
                "duplicate": True
            }
        
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{user.employee_id}_{timestamp}.jpg"
        image_path = os.path.join(settings.UPLOAD_DIR, "attendance", image_filename)
        cv2.imwrite(image_path, image)
        
        # Create attendance record (with group validation)
        try:
            attendance = attendance_service.create_attendance(
                db=db,
                user_id=user.id,
                device_id=device.id,
                confidence=confidence,
                image_path=image_path
            )
        except ValueError as e:
            # No active schedule or user not authorized
            logger.warning(f"Attendance creation failed for user {user.id}: {str(e)}")
            return {
                "success": False,
                "message": str(e),
                "recognized": True,
                "user": user.to_dict(),
                "confidence": round(confidence * 100, 2),
                "error": "no_schedule_or_unauthorized"
            }
        
        # Send Telegram notifications
        check_in_time_str = attendance.check_in_time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Admin notification (existing)
        await telegram_service.notify_attendance(
            user_name=user.full_name,
            employee_id=user.employee_id,
            check_in_time=check_in_time_str,
            confidence=confidence * 100,
            status=attendance.status
        )
        
        # Personal user notification (new)
        schedule_name = attendance.schedule.name if attendance.schedule else "Noma'lum"
        late_minutes = attendance.late_minutes if hasattr(attendance, 'late_minutes') else 0
        await telegram_service.notify_user_attendance(
            user_id=user.id,
            schedule_name=schedule_name,
            check_in_time=attendance.check_in_time.strftime("%H:%M:%S"),
            status=attendance.status,
            late_minutes=late_minutes
        )
        
        logger.info(f"Attendance recorded for {user.full_name}")
        return {
            "success": True,
            "message": "Attendance recorded successfully",
            "recognized": True,
            "user": user.to_dict(),
            "confidence": round(confidence * 100, 2),
            "attendance": attendance.to_dict(),
            "duplicate": False
        }
        
    except Exception as e:
        logger.error(f"Face recognition error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face recognition failed: {str(e)}"
        )


@router.post("/register")
async def register_face(
    user_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Register new face for a user
    
    Args:
        user_id: User ID
        file: Face image file
        db: Database session
        
    Returns:
        Created face record
    """
    # Check if user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    try:
        # Read image
        contents = await file.read()
        nparr = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if image is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid image file"
            )
        
        # Extract embedding
        embedding = face_recognition_service.get_embedding(image)
        
        if embedding is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No face detected in image"
            )
        
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        image_filename = f"{user.employee_id}_{timestamp}.jpg"
        image_path = os.path.join(settings.UPLOAD_DIR, "faces", image_filename)
        cv2.imwrite(image_path, image)
        
        # Save to database
        face = Face(
            user_id=user_id,
            embedding=face_recognition_service.embedding_to_bytes(embedding),
            image_path=image_path
        )
        
        db.add(face)
        db.commit()
        db.refresh(face)
        
        logger.info(f"Face registered for user {user.employee_id}")
        
        return {
            "success": True,
            "message": "Face registered successfully",
            "face": face.to_dict()
        }
        
    except Exception as e:
        logger.error(f"Face registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Face registration failed: {str(e)}"
        )


@router.delete("/{face_id}")
async def delete_face(face_id: int, db: Session = Depends(get_db)):
    """Delete a face record"""
    face = db.query(Face).filter(Face.id == face_id).first()
    
    if not face:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Face not found"
        )
    
    # Delete image file if exists
    if face.image_path and os.path.exists(face.image_path):
        os.remove(face.image_path)
    
    db.delete(face)
    db.commit()
    
    return {"success": True, "message": "Face deleted successfully"}


@router.get("/user/{user_id}")
async def get_user_faces(user_id: int, db: Session = Depends(get_db)):
    """Get all faces for a user"""
    faces = db.query(Face).filter(Face.user_id == user_id).all()
    
    return {
        "success": True,
        "faces": [face.to_dict() for face in faces]
    }
