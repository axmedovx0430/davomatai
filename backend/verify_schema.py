from sqlalchemy import inspect
from database import engine

def check_schema():
    inspector = inspect(engine)
    
    print("Checking 'users' table...")
    columns = [col['name'] for col in inspector.get_columns('users')]
    expected_user_columns = ['language', 'telegram_chat_id', 'course', 'major', 'faculty']
    for col in expected_user_columns:
        if col in columns:
            print(f"✅ Column '{col}' exists.")
        else:
            print(f"❌ Column '{col}' MISSING.")
            
    print("\nChecking 'schedules' table...")
    columns = [col['name'] for col in inspector.get_columns('schedules')]
    expected_schedule_columns = ['teacher', 'room']
    for col in expected_schedule_columns:
        if col in columns:
            print(f"✅ Column '{col}' exists.")
        else:
            print(f"❌ Column '{col}' MISSING.")

if __name__ == "__main__":
    check_schema()
