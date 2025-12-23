"""
Database migration utility using SQLAlchemy
"""
import logging
from sqlalchemy import text, inspect
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def add_column_if_not_exists(engine: Engine, table_name: str, column_name: str, column_type: str, default_value: str = None):
    """
    Adds a column to a table if it doesn't already exist.
    Works for both SQLite and PostgreSQL.
    """
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    if column_name not in columns:
        logger.info(f"Adding column '{column_name}' to table '{table_name}'...")
        
        # Construct ALTER TABLE statement
        alter_stmt = f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}"
        if default_value is not None:
            alter_stmt += f" DEFAULT {default_value}"
            
        with engine.connect() as conn:
            try:
                conn.execute(text(alter_stmt))
                conn.commit()
                logger.info(f"✅ Column '{column_name}' added to '{table_name}'.")
            except Exception as e:
                logger.error(f"❌ Error adding column '{column_name}': {e}")
                conn.rollback()
    else:
        logger.info(f"✅ Column '{column_name}' already exists in table '{table_name}'.")

def migrate_users_table(engine: Engine):
    """
    Run all migrations for the users table
    """
    # Language field
    add_column_if_not_exists(engine, "users", "language", "VARCHAR(10)", "'uz'")
    
    # Telegram fields
    add_column_if_not_exists(engine, "users", "telegram_chat_id", "VARCHAR(50)")
    add_column_if_not_exists(engine, "users", "telegram_username", "VARCHAR(100)")
    add_column_if_not_exists(engine, "users", "telegram_notifications", "BOOLEAN", "TRUE")
    add_column_if_not_exists(engine, "users", "telegram_registered_at", "TIMESTAMP")
    
    # Academic fields
    add_column_if_not_exists(engine, "users", "course", "INTEGER")
    add_column_if_not_exists(engine, "users", "major", "VARCHAR(255)")
    add_column_if_not_exists(engine, "users", "faculty", "VARCHAR(255)")

def migrate_schedules_table(engine: Engine):
    """
    Run all migrations for the schedules table
    """
    add_column_if_not_exists(engine, "schedules", "teacher", "VARCHAR(100)")
    add_column_if_not_exists(engine, "schedules", "room", "VARCHAR(50)")
