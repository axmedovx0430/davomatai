import sys
import os
from datetime import datetime, timedelta

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.schedule import Schedule

def fix_schedule_5():
    db = SessionLocal()
    try:
        schedule = db.query(Schedule).filter(Schedule.id == 5).first()
        if schedule:
            print(f"Before: effective_to = {schedule.effective_to}")
            
            # Set to tomorrow or remove the limit
            schedule.effective_to = datetime.now().date() + timedelta(days=30)
            
            db.commit()
            db.refresh(schedule)
            
            print(f"After: effective_to = {schedule.effective_to}")
            print("Schedule 5 updated successfully!")
        else:
            print("Schedule 5 not found!")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_schedule_5()
