"""
Migration: Add teacher and room columns to Schedule model
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
    """Add teacher and room columns to schedules table"""
    
    with engine.connect() as conn:
        try:
            # Check if columns already exist
            result = conn.execute(text("""
                SELECT COUNT(*) as count
                FROM pragma_table_info('schedules')
                WHERE name = 'teacher'
            """))
            
            teacher_exists = result.scalar() > 0
            
            if not teacher_exists:
                logger.info("Adding schedule details columns...")
                
                # Add teacher column
                logger.info("Adding teacher column...")
                conn.execute(text("""
                    ALTER TABLE schedules 
                    ADD COLUMN teacher VARCHAR(100)
                """))
                
                # Add room column
                logger.info("Adding room column...")
                conn.execute(text("""
                    ALTER TABLE schedules 
                    ADD COLUMN room VARCHAR(50)
                """))
                
                conn.commit()
                logger.info("✅ Migration completed successfully!")
            else:
                logger.info("✅ Schedule details columns already exist, skipping migration")
            
            # Verify changes
            logger.info("Verifying changes...")
            result = conn.execute(text("""
                SELECT name, type 
                FROM pragma_table_info('schedules')
                WHERE name IN ('teacher', 'room')
                ORDER BY name
            """))
            
            logger.info("New columns:")
            for row in result:
                logger.info(f"  - {row[0]}: {row[1]}")
                
        except Exception as e:
            logger.error(f"❌ Migration failed: {e}")
            conn.rollback()
            raise


if __name__ == "__main__":
    logger.info("Starting migration: Add teacher and room to Schedule model")
    migrate()
    logger.info("Migration completed!")
