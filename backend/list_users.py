from database import SessionLocal
from models.user import User

db = SessionLocal()
users = db.query(User).all()

print(f"{'ID':<5} | {'Employee ID':<15} | {'Full Name'}")
print("-" * 40)
for user in users:
    print(f"{user.id:<5} | {user.employee_id:<15} | {user.full_name}")

db.close()
