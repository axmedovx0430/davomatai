"""
Database connection and session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database - create all tables and default admin if needed
    """
    Base.metadata.create_all(bind=engine)
    
    # Create default admin if no users exist
    db = SessionLocal()
    try:
        from models.user import User
        from models.device import Device
        from datetime import datetime
        
        if db.query(User).count() == 0:
            admin = User(
                full_name="Administrator",
                employee_id="ADMIN001",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            print("Default admin user created: ADMIN001")
            
        # Create default device if none exist
        if db.query(Device).count() == 0:
            device = Device(
                device_name="Main Entrance",
                location="Default Location",
                api_key=settings.DEFAULT_DEVICE_API_KEY,
                is_active=True,
                last_seen=datetime.now()
            )
            db.add(device)
            db.commit()
            print(f"Default device created with API Key: {settings.DEFAULT_DEVICE_API_KEY}")
            
    except Exception as e:
        print(f"Error during database seeding: {e}")
    finally:
        db.close()
