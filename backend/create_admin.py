"""
Script to create admin user with password
"""
from database import SessionLocal
from models.user import User
from routes.auth_routes import hash_password
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_admin_user():
    """Create admin user with default credentials"""
    db = SessionLocal()
    try:
        # Check if admin already exists
        admin = db.query(User).filter(User.employee_id == "ADMIN001").first()
        
        if admin:
            logger.info("Admin user already exists")
            # Update password if needed
            admin.password_hash = hash_password("admin123")
            admin.role = "admin"
            db.commit()
            logger.info("Admin password updated")
        else:
            # Create new admin user
            admin = User(
                full_name="Administrator",
                employee_id="ADMIN001",
                email="admin@davomatai.uz",
                role="admin",
                password_hash=hash_password("admin123"),
                is_active=True
            )
            db.add(admin)
            db.commit()
            logger.info("Admin user created successfully")
        
        print("\n" + "="*50)
        print("ADMIN CREDENTIALS")
        print("="*50)
        print(f"Employee ID: ADMIN001")
        print(f"Password: admin123")
        print("="*50)
        print("\nIMPORTANT: Change the password after first login!")
        print("="*50 + "\n")
        
    except Exception as e:
        logger.error(f"Failed to create admin user: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
