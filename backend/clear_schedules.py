from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models.schedule import Schedule
from models.attendance import Attendance

def clear_schedules():
    db = SessionLocal()
    try:
        # First, unlink attendance records from schedules
        # This prevents foreign key constraint errors
        print("Unlinking attendance records...")
        db.query(Attendance).update({Attendance.schedule_id: None})
        
        # Now delete all schedules
        print("Deleting schedules...")
        num_deleted = db.query(Schedule).delete()
        
        db.commit()
        print(f"Successfully deleted {num_deleted} schedules.")
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    clear_schedules()
