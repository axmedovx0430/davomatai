"""
Migration script to add course, major, and faculty columns to users table
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
    logger.info("Starting migration: Add profile fields to users table")
    
    fields = [
        ("course", "INTEGER"),
        ("major", "VARCHAR(255)"),
        ("faculty", "VARCHAR(255)")
    ]

    for field_name, field_type in fields:
        add_column_if_not_exists(engine, "users", field_name, field_type)

    logger.info("Migration complete.")

if __name__ == "__main__":
    migrate()
