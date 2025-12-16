import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.user import User
from models.group import Group

def debug_attendance():
    db = SessionLocal()
    try:
        print(f"Current Time: {datetime.now()}")
        
        # Check Group 1
        group1 = db.query(Group).filter(Group.id == 1).first()
        if group1:
            print(f"Group 1: {group1.name}")
            print(f"Users in Group 1: {[u.full_name + ' (' + str(u.id) + ')' for u in group1.users]}")
        else:
            print("Group 1 not found!")

        # Check User 4
        user4 = db.query(User).filter(User.id == 4).first()
        if user4:
            print(f"User 4: {user4.full_name}")
            print(f"User 4 Groups: {[g.name + ' (' + str(g.id) + ')' for g in user4.groups]}")
            
            # Test schedule matching
            from services.attendance_service import AttendanceService
            print("\nTesting schedule matching for User 4...")
            schedule_id = AttendanceService.get_active_schedule_at_time(db, datetime.now(), user4.id)
            print(f"Result: Schedule ID {schedule_id}")
        else:
            print("User 4 not found!")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    debug_attendance()
