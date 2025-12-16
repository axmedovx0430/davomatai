"""
Utility functions
"""
from datetime import datetime, time, timedelta
from typing import Optional
import os
from config import settings


def get_upload_path(subfolder: str, filename: str) -> str:
    """
    Get full upload path for a file
    
    Args:
        subfolder: Subfolder name (faces, attendance)
        filename: File name
        
    Returns:
        Full path to file
    """
    return os.path.join(settings.UPLOAD_DIR, subfolder, filename)


def generate_filename(prefix: str, extension: str = "jpg") -> str:
    """
    Generate unique filename with timestamp
    
    Args:
        prefix: Filename prefix (e.g., employee_id)
        extension: File extension
        
    Returns:
        Unique filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def is_work_hours(check_time: Optional[datetime] = None) -> bool:
    """
    Check if current time is within work hours
    
    Args:
        check_time: Time to check (default: now)
        
    Returns:
        True if within work hours
    """
    if check_time is None:
        check_time = datetime.now()
    
    # Parse work start time
    work_start_hour, work_start_minute = map(int, settings.WORK_START_TIME.split(':'))
    work_start = time(work_start_hour, work_start_minute)
    work_end = time(18, 0)  # 6 PM
    
    current_time = check_time.time()
    
    return work_start <= current_time <= work_end


def format_confidence(confidence: float) -> str:
    """
    Format confidence as percentage string
    
    Args:
        confidence: Confidence value (0-1)
        
    Returns:
        Formatted string (e.g., "95.5%")
    """
    return f"{confidence * 100:.1f}%"


def get_status_emoji(status: str) -> str:
    """
    Get emoji for attendance status
    
    Args:
        status: Attendance status
        
    Returns:
        Emoji string
    """
    emoji_map = {
        "present": "✅",
        "late": "⏰",
        "absent": "❌"
    }
    return emoji_map.get(status, "❓")


def parse_time(time_str: Optional[str]) -> Optional[time]:
    """
    Parse time string in various formats
    
    Args:
        time_str: Time string (HH:MM or HH:MM:SS)
        
    Returns:
        time object or None
    """
    if not time_str:
        return None
        
    try:
        # Try ISO format first (HH:MM:SS)
        return time.fromisoformat(time_str)
    except ValueError:
        try:
            # Try HH:MM format
            return datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            # Try HH:MM:SS format manually if fromisoformat fails
            return datetime.strptime(time_str, "%H:%M:%S").time()


def get_current_time() -> datetime:
    """
    Get current time with timezone (UTC+5 for Uzbekistan)
    
    Returns:
        datetime object with timezone info
    """
    from datetime import timezone, timedelta
    
    # Uzbekistan is UTC+5
    tz = timezone(timedelta(hours=5))
    return datetime.now(tz)


def get_today_range() -> tuple[datetime, datetime]:
    """
    Get start and end datetime for today (in local timezone)
    
    Returns:
        (start_time, end_time) tuple
    """
    now = get_current_time()
    start_time = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=1)
    
    return start_time, end_time
