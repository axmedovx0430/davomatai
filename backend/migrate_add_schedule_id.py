"""
Database migration script to add schedule_id column to attendance table
"""
import sqlite3
import os

def migrate_database():
    db_path = os.path.join(os.path.dirname(__file__), 'attendance.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if schedule_id column already exists
        cursor.execute("PRAGMA table_info(attendance)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'schedule_id' in columns:
            print("✓ schedule_id column already exists in attendance table")
        else:
            print("Adding schedule_id column to attendance table...")
            cursor.execute("""
                ALTER TABLE attendance 
                ADD COLUMN schedule_id INTEGER 
                REFERENCES schedules(id)
            """)
            conn.commit()
            print("✓ Successfully added schedule_id column to attendance table")
        
        # Verify the change
        cursor.execute("PRAGMA table_info(attendance)")
        columns = cursor.fetchall()
        print("\nCurrent attendance table schema:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
    except sqlite3.Error as e:
        print(f"✗ Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("Starting database migration...")
    migrate_database()
    print("\nMigration complete!")
