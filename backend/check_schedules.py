"""
Jadval sozlamalarini tekshirish scripti
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.schedule import Schedule
from config import settings

# Database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

try:
    print("=== BARCHA JADVALLAR ===\n")
    schedules = db.query(Schedule).all()
    
    for schedule in schedules:
        print(f"Jadval {schedule.id}: {schedule.name}")
        print(f"  Kun: {schedule.day_of_week}")
        print(f"  Vaqt: {schedule.start_time} - {schedule.end_time}")
        print(f"  Guruh: {schedule.group_id}")
        print(f"  Kechikish chegarasi: {schedule.late_threshold_minutes} daqiqa")
        print(f"  Qayta davomat taqiqi: {schedule.duplicate_check_minutes} daqiqa")
        print(f"  O'qituvchi: {schedule.teacher}")
        print(f"  Xona: {schedule.room}")
        print(f"  Effective from: {schedule.effective_from}")
        print(f"  Effective to: {schedule.effective_to}")
        print(f"  Faol: {schedule.is_active}")
        print()
        
finally:
    db.close()
