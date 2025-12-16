import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.schedule import Schedule

def check_schedule_5():
    db = SessionLocal()
    try:
        now = datetime.now()
        print(f"Current Time: {now}")
        print(f"Current Day of Week: {now.weekday()} (0=Monday, 6=Sunday)")
        print(f"Current Time Only: {now.time()}")
        
        # Get Schedule 5
        schedule = db.query(Schedule).filter(Schedule.id == 5).first()
        if schedule:
            print(f"\nSchedule 5:")
            print(f"  Name: {schedule.name}")
            print(f"  Day of Week: {schedule.day_of_week}")
            print(f"  Start Time: {schedule.start_time}")
            print(f"  End Time: {schedule.end_time}")
            print(f"  Group ID: {schedule.group_id}")
            print(f"  Is Active: {schedule.is_active}")
            print(f"  Effective From: {schedule.effective_from}")
            print(f"  Effective To: {schedule.effective_to}")
            
            # Calculate time window
            from datetime import timedelta
            earliest = (datetime.combine(datetime.today(), schedule.start_time) - timedelta(minutes=30)).time()
            latest = schedule.end_time
            
            print(f"\nAllowed Time Window:")
            print(f"  Earliest: {earliest}")
            print(f"  Latest: {latest}")
            print(f"  Current: {now.time()}")
            print(f"  Is in window? {earliest <= now.time() <= latest}")
        else:
            print("Schedule 5 not found!")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    check_schedule_5()
