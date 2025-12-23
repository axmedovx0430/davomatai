"""
Migration: Add Telegram fields to User model
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
    """Add telegram_chat_id and telegram_notifications fields to users table"""
    logger.info("Starting migration: Add Telegram fields to User model")
    
    add_column_if_not_exists(engine, "users", "telegram_chat_id", "VARCHAR(50)")
    add_column_if_not_exists(engine, "users", "telegram_username", "VARCHAR(100)")
    add_column_if_not_exists(engine, "users", "telegram_notifications", "BOOLEAN", "TRUE")
    add_column_if_not_exists(engine, "users", "telegram_registered_at", "TIMESTAMP")
    
    logger.info("Migration completed!")


if __name__ == "__main__":
    migrate()
