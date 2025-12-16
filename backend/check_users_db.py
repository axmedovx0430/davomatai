from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os

db_path = "attendance.db"
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = SessionLocal()

try:
    print("\nUsers:")
    users = db.execute(text("SELECT id, full_name, is_active FROM users")).fetchall()
    for row in users:
        print(f"ID: {row[0]}, Name: {row[1]}, Active: {row[2]}")

finally:
    db.close()
