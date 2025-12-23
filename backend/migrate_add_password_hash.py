"""
Database migration to add password_hash field to users table
"""
from sqlalchemy import Column, String, text
from database import engine
import logging

logger = logging.getLogger(__name__)

def migrate_add_password_hash():
    """Add password_hash column to users table"""
    try:
        with engine.connect() as conn:
            # Check if column already exists
            result = conn.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='users' AND column_name='password_hash'
            """))
            
            if result.fetchone():
                logger.info("password_hash column already exists")
                return
            
            # Add password_hash column
            conn.execute(text("""
                ALTER TABLE users 
                ADD COLUMN password_hash VARCHAR(255)
            """))
            conn.commit()
            
            logger.info("Successfully added password_hash column to users table")
            
    except Exception as e:
        logger.error(f"Migration failed: {e}")
        raise

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    migrate_add_password_hash()
    print("Migration completed successfully!")
