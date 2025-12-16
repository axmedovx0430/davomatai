import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.attendance import Attendance
from models.user import User

def check_latest_attendance():
    db = SessionLocal()
    try:
        print(f"Current Time: {datetime.now()}")
        
        # Get last 5 attendance records
        records = db.query(Attendance).order_by(Attendance.check_in_time.desc()).limit(5).all()
        
        if records:
            print(f"Found {len(records)} recent records:")
            for r in records:
                user = db.query(User).filter(User.id == r.user_id).first()
                user_name = user.full_name if user else "Unknown"
                print(f" - ID: {r.id}, User: {user_name} ({r.user_id}), Time: {r.check_in_time}, Status: {r.status}")
        else:
            print("No attendance records found.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_latest_attendance()
