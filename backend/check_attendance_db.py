from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

# Check if attendance.db exists
db_path = "attendance.db"
if not os.path.exists(db_path):
    print(f"Database file {db_path} not found!")
    exit(1)

DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    # Count total records
    result = db.execute(text("SELECT COUNT(*) FROM attendance")).scalar()
    print(f"Total attendance records: {result}")
    
    # List recent records
    print("\nRecent records:")
    records = db.execute(text("SELECT id, user_id, check_in_time, status FROM attendance ORDER BY check_in_time DESC LIMIT 10")).fetchall()
    for row in records:
        print(f"ID: {row[0]}, User: {row[1]}, Time: {row[2]}, Status: {row[3]}")

finally:
    db.close()
