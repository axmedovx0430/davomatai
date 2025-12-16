from database import get_db
from models.user import User
from models.schedule import Schedule
from models.group import Group

db = next(get_db())
users = db.query(User).all()
schedules = db.query(Schedule).all()
groups = db.query(Group).all()

print(f"Users count: {len(users)}")
for u in users:
    print(f" - {u.full_name} ({u.role}) - Active: {u.is_active}")

print(f"Schedules count: {len(schedules)}")
for s in schedules:
    print(f" - {s.name} ({s.start_time}-{s.end_time})")
    # Check if schedule has days relationship or similar
    if hasattr(s, 'days'):
        print(f"   Days: {[d.day_of_week for d in s.days]}")
    else:
        print("   (No days attribute found, checking model structure needed)")

print(f"Groups count: {len(groups)}")
for g in groups:
    print(f" - {g.name} ({g.code})")
