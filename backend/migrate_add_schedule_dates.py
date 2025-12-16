import sqlite3
import os

DB_PATH = "attendance.db"

def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} not found!")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Check if columns exist
        cursor.execute("PRAGMA table_info(schedules)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if "effective_from" not in columns:
            print("Adding effective_from column...")
            cursor.execute("ALTER TABLE schedules ADD COLUMN effective_from TIMESTAMP")
        else:
            print("effective_from column already exists.")

        if "effective_to" not in columns:
            print("Adding effective_to column...")
            cursor.execute("ALTER TABLE schedules ADD COLUMN effective_to TIMESTAMP")
        else:
            print("effective_to column already exists.")

        conn.commit()
        print("Migration completed successfully!")

    except Exception as e:
        print(f"Migration failed: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate()
