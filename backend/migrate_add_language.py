"""
Migration script to add language column to users table
"""
import sqlite3
import os

def migrate():
    db_path = "attendance.db"
    if not os.path.exists(db_path):
        print(f"Database {db_path} not found.")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    try:
        # Add language column
        print("Adding 'language' column to 'users' table...")
        cursor.execute("ALTER TABLE users ADD COLUMN language VARCHAR(10) DEFAULT 'uz'")
        print("✅ Column 'language' added.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e).lower():
            print("⚠️ Column 'language' already exists.")
        else:
            print(f"❌ Error adding 'language': {e}")

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
