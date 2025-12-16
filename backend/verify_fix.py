from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from services.attendance_service import attendance_service
from datetime import datetime, timedelta
from database import get_db

# Setup DB connection
db_path = "attendance.db"
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    print("Testing get_attendance_by_date_range...")
    start_date = datetime.now() - timedelta(days=30)
    end_date = datetime.now() + timedelta(days=1)
    
    records = attendance_service.get_attendance_by_date_range(db, start_date, end_date)
    
    print(f"Found {len(records)} records for active users.")
    for r in records:
        print(f"  User: {r.user.full_name} (Active: {r.user.is_active}) - {r.check_in_time}")
        if not r.user.is_active:
            print("  ❌ ERROR: Inactive user found!")
            
    print("\nTesting get_today_attendance...")
    today_records = attendance_service.get_today_attendance(db)
    print(f"Found {len(today_records)} records for today (active users only).")
    for r in today_records:
        print(f"  User: {r.user.full_name} (Active: {r.user.is_active}) - {r.check_in_time}")
        if not r.user.is_active:
            print("  ❌ ERROR: Inactive user found!")

finally:
    db.close()
