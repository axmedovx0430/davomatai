"""
Migration: Add Telegram fields to User model
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from database import engine
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """Add telegram_chat_id and telegram_notifications fields to users table"""
    
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            result = conn.execute(text("""
                SELECT COUNT(*) as count
                FROM pragma_table_info('users')
                WHERE name = 'telegram_chat_id'
            """))
            
            telegram_chat_id_exists = result.scalar() > 0
            
            if not telegram_chat_id_exists:
                logger.info("Adding telegram fields...")
                
                # Add telegram_chat_id column
                logger.info("Adding telegram_chat_id column...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN telegram_chat_id VARCHAR(50)
                """))
                
                # Add telegram_username column
                logger.info("Adding telegram_username column...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN telegram_username VARCHAR(100)
                """))
                
                # Add telegram_notifications column
                logger.info("Adding telegram_notifications column...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN telegram_notifications BOOLEAN DEFAULT 1
                """))
                
                # Add telegram_registered_at column
                logger.info("Adding telegram_registered_at column...")
                conn.execute(text("""
                    ALTER TABLE users 
                    ADD COLUMN telegram_registered_at TIMESTAMP
                """))
                
                conn.commit()
                logger.info("✅ Migration completed successfully!")
            else:
                logger.info("✅ Telegram fields already exist, skipping migration")
            
            # Verify changes
            logger.info("Verifying changes...")
            result = conn.execute(text("""
                SELECT name, type 
                FROM pragma_table_info('users')
                WHERE name LIKE 'telegram%'
                ORDER BY name
            """))
            
            logger.info("Telegram columns:")
            for row in result:
                logger.info(f"  - {row[0]}: {row[1]}")
                
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            conn.rollback()
            raise


if __name__ == "__main__":
    logger.info("Starting migration: Add Telegram fields to User model")
    migrate()
    logger.info("Migration completed!")
