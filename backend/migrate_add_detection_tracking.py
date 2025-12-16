"""
Migratsiya: Attendance jadvaliga detection tracking ustunlarini qo'shish
"""
from sqlalchemy import create_engine, text
from config import settings

def migrate():
    engine = create_engine(settings.DATABASE_URL)
    
    with engine.connect() as conn:
        try:
            # detection_count ustunini qo'shish
            conn.execute(text("""
                ALTER TABLE attendance 
                ADD COLUMN detection_count INTEGER DEFAULT 1
            """))
            print("✅ detection_count ustuni qo'shildi")
            
            # last_seen_time ustunini qo'shish (SQLite uchun)
            conn.execute(text("""
                ALTER TABLE attendance 
                ADD COLUMN last_seen_time TIMESTAMP
            """))
            print("✅ last_seen_time ustuni qo'shildi")
            
            # Mavjud yozuvlar uchun last_seen_time ni check_in_time ga tenglashtirish
            conn.execute(text("""
                UPDATE attendance 
                SET last_seen_time = check_in_time 
                WHERE last_seen_time IS NULL
            """))
            print("✅ Mavjud yozuvlar yangilandi")
            
            conn.commit()
            print("\n🎉 Migratsiya muvaffaqiyatli yakunlandi!")
            
        except Exception as e:
            print(f"❌ Xato: {e}")
            conn.rollback()

if __name__ == "__main__":
    migrate()
