"""
Script to delete all users from the database
"""
import sqlite3
import os
import shutil

def delete_all_users():
    db_path = os.path.join(os.path.dirname(__file__), 'attendance.db')
    
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return
    
    # Create backup first
    backup_path = db_path + '.backup'
    shutil.copy2(db_path, backup_path)
    print(f"✓ Backup created at {backup_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Get count before deletion
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        if user_count == 0:
            print("Database already empty - no users to delete")
            return
        
        print(f"Found {user_count} users in database")
        
        # Check if face_encodings table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='face_encodings'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM face_encodings")
            face_count = cursor.rowcount
            print(f"✓ Deleted {face_count} face encodings")
        
        # Check if faces table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='faces'")
        if cursor.fetchone():
            cursor.execute("DELETE FROM faces")
            face_count = cursor.rowcount
            print(f"✓ Deleted {face_count} face records")
        
        # Delete all attendance records
        cursor.execute("DELETE FROM attendance")
        attendance_count = cursor.rowcount
        print(f"✓ Deleted {attendance_count} attendance records")
        
        # Delete all users
        cursor.execute("DELETE FROM users")
        deleted_count = cursor.rowcount
        
        conn.commit()
        print(f"✓ Successfully deleted {deleted_count} users")
        
        # Verify deletion
        cursor.execute("SELECT COUNT(*) FROM users")
        remaining = cursor.fetchone()[0]
        print(f"\nRemaining users: {remaining}")
        
    except sqlite3.Error as e:
        print(f"✗ Error during deletion: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    print("=" * 50)
    print("DELETING ALL USERS FROM DATABASE")
    print("=" * 50)
    
    response = input("\nAre you sure you want to delete ALL users? (yes/no): ")
    
    if response.lower() == 'yes':
        delete_all_users()
        print("\n✓ Operation complete!")
    else:
        print("\n✗ Operation cancelled")
