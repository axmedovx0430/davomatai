from database import SessionLocal
from services.attendance_service import attendance_service
from services.schedule_service import schedule_service
from models.user import User
from models.schedule import Schedule
from models.group import Group
from datetime import datetime, timedelta

def verify_fixes():
    db = SessionLocal()
    try:
        # 1. Verify Schedule Logic
        print("=== Verifying Schedule Logic ===")
        # Find a user with groups
        user = db.query(User).join(User.groups).first()
        if user:
            print(f"Testing with User: {user.full_name} (ID: {user.id})")
            schedules = schedule_service.get_user_schedules(db, user.id)
            print(f"Found {len(schedules)} schedules:")
            for s in schedules:
                print(f" - {s.name} (Group: {s.group_id})")
        else:
            print("No user with groups found.")

        # 2. Verify Stats Logic
        print("\n=== Verifying Stats Logic ===")
        if user:
            stats = attendance_service.get_user_attendance_stats(db, user.id, days=30)
            print(f"Stats for last 30 days:")
            print(f" - Total Days: {stats['total_days']}")
            print(f" - Present: {stats['present']}")
            print(f" - Late: {stats['late']}")
            print(f" - Absent: {stats['absent']}")
            print(f" - Rate: {stats['attendance_rate']}%")
            
            # Sanity check
            if stats['absent'] < 30:
                 print("✅ Absent count seems reasonable (less than 30).")
            else:
                 print("⚠️ Absent count is still high (30 or more). Check if user has schedules.")

    finally:
        db.close()

if __name__ == "__main__":
    verify_fixes()
