"""
Attendance Service
"""
from sqlalchemy.orm import Session
from models.attendance import Attendance
from models.user import User
from datetime import datetime, time, timedelta
from config import settings
from utils import get_current_time, get_today_range
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class AttendanceService:
    @staticmethod
    def check_duplicate_today(db: Session, user_id: int) -> bool:
        """
        Check if user already has attendance record for today
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            True if duplicate exists
        """
        today_start, today_end = get_today_range()
        
        existing = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_in_time >= today_start,
            Attendance.check_in_time < today_end
        ).first()
        
        return existing is not None
    
    @staticmethod
    def get_current_settings(db: Session):
        """
        Get current active time settings from database
        
        Args:
            db: Database session
            
        Returns:
            TimeSettings object or None
        """
        from models.time_settings import TimeSettings
        
        settings = db.query(TimeSettings).filter(
            TimeSettings.is_active == 1
        ).order_by(TimeSettings.created_at.desc()).first()
        
        return settings
    
    @staticmethod
    def determine_status(check_in_time: datetime, db: Session, schedule_id: Optional[int] = None) -> str:
        """
        Determine attendance status based on check-in time and dynamic settings
        
        Args:
            check_in_time: Check-in timestamp
            db: Database session
            schedule_id: Optional Schedule ID to check for specific settings
            
        Returns:
            'present' or 'late'
        """
        # Default values
        late_threshold_minutes = None
        work_start = None
        
        # 1. Check schedule-specific settings first
        if schedule_id:
            from models.schedule import Schedule
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            
            if schedule:
                # Use schedule start time
                work_start = schedule.start_time
                
                # Use schedule-specific late threshold if set
                if schedule.late_threshold_minutes is not None:
                    late_threshold_minutes = schedule.late_threshold_minutes
        
        # 2. Fallback to global settings if not determined yet
        settings = AttendanceService.get_current_settings(db)
        
        if settings:
            if not work_start:
                work_start = settings.work_start_time
            
            # Only use global late threshold if schedule didn't specify one
            if late_threshold_minutes is None:
                late_threshold_minutes = settings.late_threshold_minutes
        else:
            # Fallback to config settings
            from config import settings as config_settings
            if not work_start:
                work_start_hour, work_start_minute = map(int, config_settings.WORK_START_TIME.split(':'))
                work_start = time(work_start_hour, work_start_minute)
            
            if late_threshold_minutes is None:
                late_threshold_minutes = config_settings.LATE_THRESHOLD_MINUTES
        
        # Calculate late threshold
        late_threshold = datetime.combine(
            check_in_time.date(),
            work_start
        ) + timedelta(minutes=late_threshold_minutes)
        
        # Make late_threshold timezone aware if check_in_time is
        if check_in_time.tzinfo is not None and late_threshold.tzinfo is None:
            late_threshold = late_threshold.replace(tzinfo=check_in_time.tzinfo)
        
        if check_in_time <= late_threshold:
            return "present"
        else:
            return "late"
    
    @staticmethod
    def get_active_schedule_at_time(db: Session, check_time: datetime, user_id: Optional[int] = None) -> Optional[int]:
        """
        Find active schedule for the given time
        If user_id is provided, only returns schedules the user is authorized to attend
        
        Args:
            db: Database session
            check_time: Time to check
            user_id: Optional user ID for group-based filtering
            
        Returns:
            Schedule ID or None
        """
        # 0=Monday, 6=Sunday
        day_of_week = check_time.weekday()
        current_time = check_time.time()
        current_date = check_time.date()
        
        logger.info(f"=== JADVAL QIDIRUV BOSHLANDI ===")
        logger.info(f"Vaqt: {check_time}")
        logger.info(f"Hafta kuni: {day_of_week} (0=Dushanba, 6=Yakshanba)")
        logger.info(f"Joriy vaqt: {current_time}")
        logger.info(f"Joriy sana: {current_date}")
        
        # Find matching schedule
        # We import here to avoid circular imports
        from models.schedule import Schedule
        from models.user import User
        
        # LOGICAL ERROR FIX #4: Allow early arrival (30 minutes before class)
        # and prevent attendance after class ends
        early_arrival_minutes = 30
        
        # First, get ALL schedules for debugging
        all_schedules = db.query(Schedule).all()
        logger.info(f"Bazada jami {len(all_schedules)} ta jadval mavjud")
        
        # Get schedules for this day
        day_schedules = db.query(Schedule).filter(
            Schedule.day_of_week == day_of_week
        ).all()
        logger.info(f"Hafta kuni {day_of_week} uchun {len(day_schedules)} ta jadval topildi")
        for s in day_schedules:
            logger.info(f"  Jadval {s.id}: {s.name}, vaqt: {s.start_time}-{s.end_time}, guruh: {s.group_id}, faol: {s.is_active}, effective_from: {s.effective_from}, effective_to: {s.effective_to}")
        
        # Get all schedules for this day
        query = db.query(Schedule).filter(
            Schedule.day_of_week == day_of_week,
            Schedule.is_active == True
        )
        
        
        # Filter by effective dates
        from sqlalchemy import or_, and_
        from datetime import datetime as dt
        
        active_schedules = query.all()
        logger.info(f"is_active=True filtridan keyin: {len(active_schedules)} ta jadval")
        
        # Convert current date to datetime for comparison (start of day)
        # effective_from and effective_to are stored as datetime, so we need to compare with datetime
        current_date_start = dt.combine(current_date, dt.min.time())
        current_date_end = dt.combine(current_date, dt.max.time())
        
        logger.info(f"Sana solishtirish: current_date_start={current_date_start}, current_date_end={current_date_end}")
        
        query = query.filter(
            and_(
                or_(Schedule.effective_from.is_(None), Schedule.effective_from <= current_date_end),
                or_(Schedule.effective_to.is_(None), Schedule.effective_to >= current_date_start)
            )
        )
        
        date_filtered_schedules = query.all()
        logger.info(f"Sana filtridan keyin: {len(date_filtered_schedules)} ta jadval")
        for s in date_filtered_schedules:
            logger.info(f"  Jadval {s.id}: effective_from={s.effective_from}, effective_to={s.effective_to}, joriy_sana={current_date}")
        
        # If user_id provided, filter by user's groups
        user_group_ids = []
        if user_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                logger.info(f"Foydalanuvchi: {user.id} ({user.full_name})")
                if user.groups:
                    user_group_ids = [g.id for g in user.groups]
                    logger.info(f"Foydalanuvchi {user.id} guruhlari: {user_group_ids}")
                else:
                    logger.info(f"Foydalanuvchi {user.id} guruhga tegishli emas")
            
                # Only schedules for user's groups OR schedules without group (public)
                before_group_filter = query.all()
                logger.info(f"Guruh filtridan oldin: {len(before_group_filter)} ta jadval")
                
                query = query.filter(
                    (Schedule.group_id.in_(user_group_ids)) | (Schedule.group_id == None)
                )
            else:
                logger.warning(f"Foydalanuvchi {user_id} topilmadi")
        
        schedules = query.all()
        logger.info(f"YAKUNIY NATIJA: Hafta kuni {day_of_week} uchun {len(schedules)} ta mos jadval topildi")
        
        if len(schedules) == 0:
            logger.warning(f"OGOHLANTIRISH: Hech qanday jadval topilmadi!")
            logger.warning(f"Qidiruv parametrlari: day_of_week={day_of_week}, is_active=True, sana={current_date}, guruhlar={user_group_ids}")
        
        # Sort schedules to prioritize group-specific ones (group_id is not None)
        # and then by start time
        schedules.sort(key=lambda s: (s.group_id is None, s.start_time))
        
        # Find schedule within valid time range
        for schedule in schedules:
            # Check if schedule has specific settings
            time_settings = AttendanceService.get_current_settings(db)
            late_threshold = schedule.late_threshold_minutes or (time_settings.late_threshold_minutes if time_settings else 30)
            
            # Allow check-in 30 mins before start
            earliest_time = (datetime.combine(check_time.date(), schedule.start_time) - timedelta(minutes=30))
            # Allow check-in until end time
            latest_time = datetime.combine(check_time.date(), schedule.end_time)
            
            # Handle midnight crossing schedules
            # If earliest_time is before midnight but schedule starts after midnight
            if earliest_time.date() < check_time.date():
                # This means we crossed midnight backwards (e.g., 23:30 for 00:00 start)
                # We need to check if current time is either:
                # 1. After earliest_time on previous day (23:30-23:59)
                # 2. Before latest_time on current day (00:00-end_time)
                
                # Check if we're in the late evening window (previous day)
                if current_time >= earliest_time.time():
                    # We're in the pre-midnight window
                    pass  # Continue to group check
                # Check if we're in the early morning window (current day)
                elif current_time <= latest_time.time():
                    # We're in the post-midnight window
                    pass  # Continue to group check
                else:
                    logger.info(f"Checking Schedule {schedule.id}: {schedule.start_time}-{schedule.end_time} (Group: {schedule.group_id})")
                    logger.info(f"  Skipping: Time {current_time} not in midnight-crossing window")
                    continue
            else:
                # Normal case: no midnight crossing
                if not (earliest_time.time() <= current_time <= latest_time.time()):
                    logger.info(f"Checking Schedule {schedule.id}: {schedule.start_time}-{schedule.end_time} (Group: {schedule.group_id})")
                    logger.info(f"  Skipping: Time {current_time} not in window {earliest_time.time()}-{latest_time.time()}")
                    continue
            
            logger.info(f"Checking Schedule {schedule.id}: {schedule.start_time}-{schedule.end_time} (Group: {schedule.group_id})")
            logger.info(f"  Window: {earliest_time.time()} - {latest_time.time()} vs Current: {current_time}")
            
            # Double check group authorization if it's a group schedule
            if schedule.group_id and user_id:
                 if schedule.group_id not in user_group_ids:
                     logger.info(f"  Skipping: Schedule Group {schedule.group_id} not in User Groups {user_group_ids}")
                     continue
            
            logger.info(f"  MATCH: Schedule {schedule.id}")
            return schedule.id
        
        logger.info("No matching schedule found in loop")
        return None
    
    @staticmethod
    def check_duplicate_attendance(db: Session, user_id: int, schedule_id: Optional[int] = None) -> tuple[bool, Attendance]:
        """
        Check if user has recent attendance record
        If schedule_id is provided, checks if user already attended this specific schedule TODAY
        within the class time range (not just any time today)
        
        Args:
            db: Database session
            user_id: User ID
            schedule_id: Optional Schedule ID
            
        Returns:
            Tuple of (is_duplicate, last_attendance_record)
        """
        logger.info(f"=== TAKRORIY DAVOMAT TEKSHIRUVI ===")
        logger.info(f"Foydalanuvchi: {user_id}, Jadval: {schedule_id}")
        
        current_time = get_current_time()
        
        # LOGICAL ERROR FIX #5: Check within class time range, not just today
        if schedule_id:
            from models.schedule import Schedule
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            
            if schedule:
                logger.info(f"Jadval topildi: {schedule.name}")
                logger.info(f"Jadval sozlamalari: duplicate_check_minutes={schedule.duplicate_check_minutes}")
                
                # Get today's date
                today = current_time.date()
                
                # Calculate class time range for today
                class_start = datetime.combine(today, schedule.start_time)
                class_end = datetime.combine(today, schedule.end_time)
                
                # Make them timezone aware if they aren't
                if class_start.tzinfo is None:
                    class_start = class_start.replace(tzinfo=current_time.tzinfo)
                if class_end.tzinfo is None:
                    class_end = class_end.replace(tzinfo=current_time.tzinfo)
                
                # Allow early arrival (30 minutes before)
                early_arrival_minutes = 30
                earliest_allowed = class_start - timedelta(minutes=early_arrival_minutes)
                
                logger.info(f"Dars vaqti oralig'i: {earliest_allowed} - {class_end}")
                
                # Check if user already attended THIS schedule within THIS class time range
                # We strictly check for the SAME schedule_id
                existing = db.query(Attendance).filter(
                    Attendance.user_id == user_id,
                    Attendance.schedule_id == schedule_id,
                    Attendance.check_in_time >= earliest_allowed,
                    Attendance.check_in_time <= class_end
                ).first()
                
                if existing:
                    logger.info(f"Dars vaqti oralig'ida davomat topildi (ID: {existing.id})")
                    logger.info(f"Birinchi davomat: {existing.check_in_time}")
                    logger.info(f"Oxirgi ko'rilgan: {existing.last_seen_time}")
                    
                    # Check if duplicate_check_minutes has passed since last_seen_time
                    duplicate_check_minutes = schedule.duplicate_check_minutes
                    if duplicate_check_minutes is None:
                        # Use global settings
                        settings_obj = AttendanceService.get_current_settings(db)
                        duplicate_check_minutes = settings_obj.duplicate_check_minutes if settings_obj else 60
                    
                    logger.info(f"Duplicate check: {duplicate_check_minutes} daqiqa")
                    
                    # Ensure last_seen_time is timezone aware for comparison
                    last_seen = existing.last_seen_time
                    if last_seen.tzinfo is None:
                        # Assume it's in the same timezone as current_time
                        last_seen = last_seen.replace(tzinfo=current_time.tzinfo)
                    
                    time_since_last = current_time - last_seen
                    minutes_since_last = time_since_last.total_seconds() / 60
                    
                    logger.info(f"Oxirgi ko'rilgandan beri: {minutes_since_last:.1f} daqiqa")
                    
                    if minutes_since_last >= duplicate_check_minutes:
                        # Enough time has passed - should update
                        logger.info(f"✅ Vaqt o'tgan - yangilash kerak")
                        return True, existing, True  # (is_duplicate, record, should_update)
                    else:
                        # Not enough time - reject
                        logger.warning(f"❌ Vaqt o'tmagan - rad etish")
                        return True, existing, False  # (is_duplicate, record, should_update)
                else:
                    logger.info(f"Dars vaqti oralig'ida takroriy davomat yo'q")
                    # IMPORTANT: If we are in a specific schedule, we do NOT fall back to global time check
                    # because that would merge attendance with previous classes.
                    # If it's a new schedule, it's a NEW attendance.
                    return False, None, False

        # Fallback to time-based check ONLY if no schedule_id provided (legacy/manual mode)
        if not schedule_id:
            logger.info(f"Jadval aniqlanmadi - vaqtga asoslangan tekshiruvga o'tish...")

        
        if schedule_id:
            from models.schedule import Schedule
            schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
            if schedule and schedule.duplicate_check_minutes is not None:
                duplicate_check_minutes = schedule.duplicate_check_minutes
                logger.info(f"Jadval sozlamasi ishlatildi: {duplicate_check_minutes} daqiqa")
        
        # If not set in schedule, get from global settings
        if duplicate_check_minutes is None:
            settings = AttendanceService.get_current_settings(db)
            
            if settings:
                duplicate_check_minutes = settings.duplicate_check_minutes
                logger.info(f"Global sozlama ishlatildi: {duplicate_check_minutes} daqiqa")
            else:
                # Default: check for today only (legacy behavior)
                duplicate_check_minutes = 60  # Default 60 mins
                logger.info(f"Default sozlama ishlatildi: {duplicate_check_minutes} daqiqa")
        
        # Calculate time window
        check_from = current_time - timedelta(minutes=duplicate_check_minutes)
        
        logger.info(f"Tekshirish oralig'i: {check_from} dan hozirgi vaqtgacha")
        
        # Find last attendance within window
        last_attendance = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_in_time >= check_from
        ).order_by(Attendance.check_in_time.desc()).first()
        
        if last_attendance:
            logger.warning(f"TAKRORIY DAVOMAT TOPILDI (Vaqt oralig'ida)!")
            logger.warning(f"Oldingi davomat: {last_attendance.check_in_time}")
            return True, last_attendance, False  # Don't update in fallback mode
        else:
            logger.info(f"Takroriy davomat yo'q - yangi davomat yaratiladi")
            return False, None, False
    
    @staticmethod
    def create_attendance(
        db: Session,
        user_id: int,
        device_id: int,
        confidence: float,
        image_path: str = None
    ) -> Attendance:
        """
        Create new attendance record with duplicate check and group validation
        
        Args:
            db: Database session
            user_id: User ID
            device_id: Device ID
            confidence: Recognition confidence
            image_path: Path to captured image
            
        Returns:
            Created Attendance object or existing one if duplicate
            
        Raises:
            ValueError: If no active schedule found or user not authorized
        """
        from models.user import User
        from models.schedule import Schedule
        
        check_in_time = get_current_time()
        
        # 1. Determine current schedule (with user group validation)
        schedule_id = AttendanceService.get_active_schedule_at_time(db, check_in_time, user_id)
        
        # LOGICAL ERROR FIX #3: Check if schedule exists
        if not schedule_id:
            logger.warning(f"No active schedule found at {check_in_time} for user {user_id}")
            raise ValueError("Hozir hech qanday dars yo'q yoki siz bu darsga ruxsatingiz yo'q")
        
        # LOGICAL ERROR FIX #2: Validate user is in the schedule's group
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        if schedule and schedule.group_id:
            user = db.query(User).filter(User.id == user_id).first()
            if user:
                user_group_ids = [g.id for g in user.groups]
                if schedule.group_id not in user_group_ids:
                    logger.warning(f"User {user_id} not authorized for schedule {schedule_id} (group {schedule.group_id})")
                    raise ValueError(f"Siz '{schedule.name}' darsiga ruxsatingiz yo'q (guruh mos emas)")
        
        # 2. Check for duplicate attendance
        is_duplicate, last_attendance, should_update = AttendanceService.check_duplicate_attendance(db, user_id, schedule_id)
        
        if is_duplicate:
            if should_update:
                # Update existing attendance
                logger.info(f"✅ Davomatni yangilash: user {user_id}")
                last_attendance.detection_count += 1
                last_attendance.last_seen_time = check_in_time
                # Update confidence if new one is higher
                if confidence > last_attendance.confidence:
                    last_attendance.confidence = confidence
                # Update image path to latest
                if image_path:
                    last_attendance.image_path = image_path
                
                db.commit()
                db.refresh(last_attendance)
                
                logger.info(f"Davomat yangilandi: count={last_attendance.detection_count}, last_seen={last_attendance.last_seen_time}")
                return last_attendance
            else:
                # Reject duplicate
                logger.info(f"❌ Takroriy davomat rad etildi: user {user_id}. Last: {last_attendance.check_in_time}")
                return last_attendance
        
        status = AttendanceService.determine_status(check_in_time, db, schedule_id)
        
        attendance = Attendance(
            user_id=user_id,
            device_id=device_id,
            check_in_time=check_in_time,
            confidence=confidence,
            image_path=image_path,
            status=status,
            schedule_id=schedule_id,  # Link to schedule
            detection_count=1,  # First detection
            last_seen_time=check_in_time  # Same as check_in_time initially
        )
        
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
        
        logger.info(f"Attendance created for user {user_id}: {status} at {check_in_time} (Schedule: {schedule_id})")
        
        return attendance
    
    @staticmethod
    def get_today_attendance(db: Session):
        """Get all attendance records for today"""
        today_start, today_end = get_today_range()
        
        return db.query(Attendance).join(User).filter(
            Attendance.check_in_time >= today_start,
            Attendance.check_in_time < today_end,
            User.is_active == True
        ).order_by(Attendance.check_in_time.desc()).all()
    
    @staticmethod
    def get_attendance_by_date_range(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        user_id: int = None,
        group_id: int = None
    ):
        """Get attendance records for date range"""
        query = db.query(Attendance).join(User).filter(
            Attendance.check_in_time >= start_date,
            Attendance.check_in_time < end_date,
            User.is_active == True
        )
        
        if user_id:
            query = query.filter(Attendance.user_id == user_id)
            
        if group_id:
            from models.group import Group
            query = query.join(User.groups).filter(Group.id == group_id)
        
        return query.order_by(Attendance.check_in_time.desc()).all()
    
    @staticmethod
    def get_user_attendance_stats(db: Session, user_id: int, days: int = 30):
        """
        Get attendance statistics for a user
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            Dictionary with statistics
        """
        start_date = get_current_time() - timedelta(days=days)
        
        records = db.query(Attendance).filter(
            Attendance.user_id == user_id,
            Attendance.check_in_time >= start_date
        ).all()
        
        total_days = days
        present_count = len([r for r in records if r.status == "present"])
        late_count = len([r for r in records if r.status == "late"])
        absent_count = total_days - len(records)
        
        return {
            "total_days": total_days,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "attendance_rate": round((len(records) / total_days) * 100, 2) if total_days > 0 else 0
        }


# Global instance
attendance_service = AttendanceService()
