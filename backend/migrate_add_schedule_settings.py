"""
Migration script to add settings columns to schedules table
"""
import sqlite3
import os

def migrate():
    db_path = os.path.join(os.path.dirname(__file__), 'attendance.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
        
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Starting migration...")
    
    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(schedules)")
        columns = [info[1] for info in cursor.fetchall()]
        
        # Add late_threshold_minutes if not exists
        if 'late_threshold_minutes' not in columns:
            print("Adding late_threshold_minutes column...")
            cursor.execute("ALTER TABLE schedules ADD COLUMN late_threshold_minutes INTEGER")
            print("✓ Added late_threshold_minutes")
        else:
            print("late_threshold_minutes already exists")
            
        # Add duplicate_check_minutes if not exists
        if 'duplicate_check_minutes' not in columns:
            print("Adding duplicate_check_minutes column...")
            cursor.execute("ALTER TABLE schedules ADD COLUMN duplicate_check_minutes INTEGER")
            print("✓ Added duplicate_check_minutes")
        else:
            print("duplicate_check_minutes already exists")
            
        conn.commit()
        print("\nMigration complete!")
        
        # Verify schema
        cursor.execute("PRAGMA table_info(schedules)")
        print("\nCurrent schedules table schema:")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
            
    except sqlite3.Error as e:
        print(f"Error during migration: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
