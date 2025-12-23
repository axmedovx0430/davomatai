"""
Migration: Add teacher and room columns to Schedule model
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import engine
from utils.migrations import add_column_if_not_exists
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def migrate():
    """Add teacher and room columns to schedules table"""
    logger.info("Starting migration: Add teacher and room to Schedule model")
    
    add_column_if_not_exists(engine, "schedules", "teacher", "VARCHAR(100)")
    add_column_if_not_exists(engine, "schedules", "room", "VARCHAR(50)")
    
    logger.info("Migration completed!")


if __name__ == "__main__":
    migrate()
