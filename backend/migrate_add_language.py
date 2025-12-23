"""
Migration script to add language column to users table
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
    logger.info("Starting migration: Add language column to users table")
    add_column_if_not_exists(engine, "users", "language", "VARCHAR(10)", "'uz'")
    logger.info("Migration complete.")

if __name__ == "__main__":
    migrate()
