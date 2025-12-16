from database import SessionLocal
from models.user import User

def seed_user():
    db = SessionLocal()
    try:
        # Check if user exists
        existing = db.query(User).filter(User.employee_id == "ADMIN001").first()
        if existing:
            print(f"User already exists: {existing.full_name} ({existing.employee_id})")
            return

        # Create user
        user = User(
            full_name="Admin User",
            employee_id="ADMIN001",
            role="admin",
            is_active=True
        )
        db.add(user)
        db.commit()
        print(f"User created successfully: {user.full_name} ({user.employee_id})")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_user()
