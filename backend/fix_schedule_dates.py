"""
Jadval 5 ning effective_to sanasini tuzatish
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
    # Jadval 5 ni topish
    schedule = db.query(Schedule).filter(Schedule.id == 5).first()
    
    if schedule:
        print(f"Topildi: Jadval {schedule.id} - {schedule.name}")
        print(f"  Hozirgi effective_from: {schedule.effective_from}")
        print(f"  Hozirgi effective_to: {schedule.effective_to}")
        
        # effective_to ni NULL qilish (cheksiz amal qiladi)
        schedule.effective_to = None
        
        db.commit()
        print(f"\n✅ TUZATILDI!")
        print(f"  Yangi effective_from: {schedule.effective_from}")
        print(f"  Yangi effective_to: {schedule.effective_to} (NULL = cheksiz)")
    else:
        print("❌ Jadval 5 topilmadi!")
        
finally:
    db.close()
