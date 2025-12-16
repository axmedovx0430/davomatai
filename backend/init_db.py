"""
Database initialization script
Run this to create initial admin user and device
"""
from database import SessionLocal, init_db
from models.user import User
from models.device import Device
from middleware.auth_middleware import generate_api_key
from datetime import datetime
import sys


def create_initial_data():
    """Create initial admin user and device"""
    db = SessionLocal()
    
    try:
        # Initialize database tables
        print("Creating database tables...")
        init_db()
        
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.role == "admin").first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.employee_id}")
        else:
            # Create admin user
            admin = User(
                full_name="Admin User",
                employee_id="ADMIN001",
                email="admin@example.com",
                phone="+998901234567",
                role="admin",
                is_active=True
            )
            db.add(admin)
            db.commit()
            db.refresh(admin)
            print(f"✅ Admin user created: {admin.employee_id}")
        
        # Check if device already exists
        existing_device = db.query(Device).first()
        if existing_device:
            print(f"Device already exists: {existing_device.device_name}")
        else:
            # Create initial device
            api_key = generate_api_key()
            device = Device(
                device_name="Main Entrance",
                location="Building A, Floor 1",
                api_key=api_key,
                is_active=True,
                last_seen=datetime.now()
            )
            db.add(device)
            db.commit()
            db.refresh(device)
            
            print(f"✅ Device created: {device.device_name}")
            print(f"📝 Device API Key: {api_key}")
            print(f"⚠️  Save this API key! It won't be shown again.")
            print(f"   Add it to esp32-cam/config.h")
        
        # Check if time settings exist
        from models.time_settings import TimeSettings
        from datetime import time as dt_time
        
        existing_settings = db.query(TimeSettings).filter(TimeSettings.is_active == 1).first()
        if existing_settings:
            print(f"Time settings already exist")
        else:
            # Create default time settings
            default_settings = TimeSettings(
                work_start_time=dt_time(9, 0),  # 09:00
                late_threshold_minutes=30,
                duplicate_check_minutes=120,  # 2 hours
                is_active=1
            )
            db.add(default_settings)
            db.commit()
            db.refresh(default_settings)
            print(f"✅ Default time settings created:")
            print(f"   - Work start time: 09:00")
            print(f"   - Late threshold: 30 minutes")
            print(f"   - Duplicate check: 120 minutes (2 hours)")
        
        print("\n✅ Database initialization complete!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    create_initial_data()
