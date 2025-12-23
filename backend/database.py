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
    except Exception as e:
        print(f"Error creating default admin: {e}")
    finally:
        db.close()
