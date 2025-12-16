import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.user import User
from models.group import Group

def fix_user_group():
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.id == 1).first()
        group = db.query(Group).filter(Group.id == 1).first()
        
        if user and group:
            if group not in user.groups:
                user.groups.append(group)
                db.commit()
                print(f"Successfully added User {user.full_name} (ID: 1) to Group {group.name} (ID: 1)")
            else:
                print(f"User {user.full_name} is already in Group {group.name}")
        else:
            print("User or Group not found")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    fix_user_group()
