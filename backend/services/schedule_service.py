"""
Schedule Service - Business logic for class schedules
"""
from sqlalchemy.orm import Session
from models.schedule import Schedule
from models.attendance import Attendance
from models.user import User
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ScheduleService:
    @staticmethod
    def create_schedule(
        db: Session,
        name: str,
        day_of_week: int,
        start_time: time,
        end_time: time,
        group_id: Optional[int] = None,
        late_threshold_minutes: Optional[int] = None,
        duplicate_check_minutes: Optional[int] = None,
        effective_from: Optional[date] = None,
        effective_to: Optional[date] = None,
        teacher: Optional[str] = None,
        room: Optional[str] = None
    ) -> Schedule:
        """
        Create a new class schedule
        
        Args:
            db: Database session
            name: Class/subject name
            day_of_week: 0=Monday, 6=Sunday
            start_time: Class start time
            end_time: Class end time
            group_id: Optional group ID
            late_threshold_minutes: Optional custom late threshold
            duplicate_check_minutes: Optional custom duplicate check interval
            effective_from: Start date of the schedule
            effective_to: End date of the schedule
            teacher: Teacher name
            room: Room number/name
            
        Returns:
            Created Schedule object
        """
        schedule = Schedule(
            name=name,
            day_of_week=day_of_week,
            start_time=start_time,
            end_time=end_time,
            group_id=group_id,
            late_threshold_minutes=late_threshold_minutes,
            duplicate_check_minutes=duplicate_check_minutes,
            effective_from=effective_from,
            effective_to=effective_to,
            teacher=teacher,
            room=room
        )
        
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        
        logger.info(f"Schedule created: {name} on day {day_of_week} at {start_time}-{end_time}")
        
        return schedule
    
    @staticmethod
    def get_week_schedules(
        db: Session, 
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> Dict[int, List[Schedule]]:
        """
        Get all active schedules organized by day of week, optionally filtered by date range
        
        Args:
            db: Database session
            start_date: Start of the week (Monday)
            end_date: End of the week (Sunday)
            
        Returns:
            Dictionary with day_of_week as key (0=Monday to 6=Sunday) 
            and list of schedules as value
        """
        query = db.query(Schedule).filter(Schedule.is_active == True)
        
        # Filter by effective dates if provided
        if start_date and end_date:
            # Logic: Schedule is valid if:
            # 1. effective_from is None OR effective_from <= end_date
            # AND
            # 2. effective_to is None OR effective_to >= start_date
            from sqlalchemy import or_, and_
            
            query = query.filter(
                and_(
                    or_(Schedule.effective_from.is_(None), Schedule.effective_from <= end_date),
                    or_(Schedule.effective_to.is_(None), Schedule.effective_to >= start_date)
                )
            )
            
        schedules = query.order_by(Schedule.day_of_week, Schedule.start_time).all()
        
        # Organize by day
        week_schedule = {i: [] for i in range(7)}  # 0=Monday to 6=Sunday
        
        for schedule in schedules:
            week_schedule[schedule.day_of_week].append(schedule)
        
        return week_schedule
    
    @staticmethod
    def get_schedule_by_id(db: Session, schedule_id: int) -> Optional[Schedule]:
        """Get schedule by ID"""
        return db.query(Schedule).filter(Schedule.id == schedule_id).first()
    
    @staticmethod
    def update_schedule(
        db: Session,
        schedule_id: int,
        name: Optional[str] = None,
        day_of_week: Optional[int] = None,
        start_time: Optional[time] = None,
        end_time: Optional[time] = None,
        group_id: Optional[int] = None,
        is_active: Optional[bool] = None,
        late_threshold_minutes: Optional[int] = None,
        duplicate_check_minutes: Optional[int] = None,
        effective_from: Optional[date] = None,
        effective_to: Optional[date] = None,
        teacher: Optional[str] = None,
        room: Optional[str] = None
    ) -> Optional[Schedule]:
        """
        Update existing schedule
        
        Args:
            db: Database session
            schedule_id: Schedule ID
            name: New name (optional)
            day_of_week: New day (optional)
            start_time: New start time (optional)
            end_time: New end time (optional)
            group_id: New group ID (optional)
            is_active: Active status (optional)
            late_threshold_minutes: New late threshold (optional)
            duplicate_check_minutes: New duplicate check interval (optional)
            effective_from: New start date (optional)
            effective_to: New end date (optional)
            teacher: New teacher name (optional)
            room: New room number (optional)
            
        Returns:
            Updated Schedule object or None
        """
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        
        if not schedule:
            return None
        
        if name is not None:
            schedule.name = name
        if day_of_week is not None:
            schedule.day_of_week = day_of_week
        if start_time is not None:
            schedule.start_time = start_time
        if end_time is not None:
            schedule.end_time = end_time
        if group_id is not None:
            schedule.group_id = group_id
        if is_active is not None:
            schedule.is_active = is_active
        if late_threshold_minutes is not None:
            schedule.late_threshold_minutes = late_threshold_minutes
        if duplicate_check_minutes is not None:
            schedule.duplicate_check_minutes = duplicate_check_minutes
        if effective_from is not None:
            schedule.effective_from = effective_from
        if effective_to is not None:
            schedule.effective_to = effective_to
        if teacher is not None:
            schedule.teacher = teacher
        if room is not None:
            schedule.room = room
        
        db.commit()
        db.refresh(schedule)
        
        logger.info(f"Schedule updated: {schedule.id}")
        
        return schedule
    
    @staticmethod
    def delete_schedule(db: Session, schedule_id: int) -> bool:
        """
        Delete schedule
        
        Args:
            db: Database session
            schedule_id: Schedule ID
            
        Returns:
            True if deleted, False if not found
        """
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        
        if not schedule:
            return False
        
        db.delete(schedule)
        db.commit()
        
        logger.info(f"Schedule deleted: {schedule_id}")
        
        return True
    
    @staticmethod
    def get_schedule_stats(db: Session, schedule_id: int, target_date: date) -> Dict:
        """
        Get attendance statistics for a specific class on a specific date
        
        Args:
            db: Database session
            schedule_id: Schedule ID
            target_date: Date to check
            
        Returns:
            Dictionary with stats
        """
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        
        if not schedule:
            return {
                "total_users": 0,
                "present": 0,
                "late": 0,
                "absent": 0
            }
        
        # Get date range for the target date
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)
        
        # Get attendance records for this schedule on this date
        attendance_records = db.query(Attendance).filter(
            Attendance.schedule_id == schedule_id,
            Attendance.check_in_time >= start_datetime,
            Attendance.check_in_time < end_datetime
        ).all()
        
        # Count by status
        present_count = len([r for r in attendance_records if r.status == "present"])
        late_count = len([r for r in attendance_records if r.status == "late"])
        
        # Get total users (from group if linked, otherwise all active users)
        if schedule.group_id:
            from models.group import Group
            total_users = db.query(User).join(
                User.groups
            ).filter(
                Group.id == schedule.group_id,
                User.is_active == True
            ).count()
        else:
            total_users = db.query(User).filter(User.is_active == True).count()
        
        # Count unique users, not total records
        unique_user_ids = set([r.user_id for r in attendance_records])
        absent_count = total_users - len(unique_user_ids)
        
        return {
            "total_users": total_users,
            "present": present_count,
            "late": late_count,
            "absent": absent_count,
            "attendance_rate": round((len(unique_user_ids) / total_users) * 100, 2) if total_users > 0 else 0
        }
    
    @staticmethod
    def get_attendance_by_schedule(
        db: Session,
        schedule_id: int,
        target_date: date
    ) -> List[Attendance]:
        """
        Get all attendance records for a specific class on a specific date
        
        Args:
            db: Database session
            schedule_id: Schedule ID
            target_date: Date to check
            
        Returns:
            List of Attendance objects (only for users in the schedule's group if applicable)
        """
        start_datetime = datetime.combine(target_date, datetime.min.time())
        end_datetime = start_datetime + timedelta(days=1)
        
        # Get the schedule to check if it has a group
        schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
        
        if not schedule:
            return []
        
        # Base query: attendance for this schedule on this date
        query = db.query(Attendance).filter(
            Attendance.schedule_id == schedule_id,
            Attendance.check_in_time >= start_datetime,
            Attendance.check_in_time < end_datetime
        )
        
        # If schedule has a group, filter by group membership
        if schedule.group_id:
            from models.group import Group
            # Join with User and their groups to filter by group membership
            query = query.join(User, Attendance.user_id == User.id).join(
                User.groups
            ).filter(
                Group.id == schedule.group_id
            )
        
        return query.order_by(Attendance.check_in_time.desc()).all()


# Global instance
schedule_service = ScheduleService()
