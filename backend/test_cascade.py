from database import get_db, Base, engine
from models.group import Group
from models.schedule import Schedule
from models.attendance import Attendance
from models.user import User
from datetime import datetime, time

# Create tables if not exist (to ensure constraints are applied if new)
# Base.metadata.create_all(bind=engine)

db = next(get_db())

def test_cascade():
    print("--- Testing Cascade Delete ---")
    
    # 1. Create Data
    print("Creating test data...")
    group = Group(name="Test Cascade Group", code="TCG-001")
    db.add(group)
    db.commit()
    db.refresh(group)
    
    schedule = Schedule(
        name="Test Schedule", 
        day_of_week=1, 
        start_time=time(9,0), 
        end_time=time(10,0), 
        group_id=group.id
    )
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    
    # Need a user for attendance
    user = db.query(User).first()
    if not user:
        print("No user found, skipping attendance test")
        return

    attendance = Attendance(
        user_id=user.id,
        schedule_id=schedule.id,
        status="present",
        confidence=0.99
    )
    db.add(attendance)
    db.commit()
    db.refresh(attendance)
    
    print(f"Created Group ID: {group.id}")
    print(f"Created Schedule ID: {schedule.id}")
    print(f"Created Attendance ID: {attendance.id}")
    
    # 2. Delete Group
    print("Deleting Group...")
    db.delete(group)
    db.commit()
    
    # 3. Verify Deletion
    print("Verifying deletion...")
    
    s_check = db.query(Schedule).filter_by(id=schedule.id).first()
    a_check = db.query(Attendance).filter_by(id=attendance.id).first()
    
    if s_check is None:
        print("✅ Schedule deleted successfully")
    else:
        print("❌ Schedule STILL EXISTS")
        
    if a_check is None:
        print("✅ Attendance deleted successfully")
    else:
        print("❌ Attendance STILL EXISTS")

if __name__ == "__main__":
    try:
        test_cascade()
    except Exception as e:
        print(f"Error: {e}")
