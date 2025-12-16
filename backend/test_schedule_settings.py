"""
Test script for schedule settings
"""
import requests
import json

API_URL = "http://localhost:8000"

def test_create_schedule_with_settings():
    """Test creating schedule with custom settings"""
    print("=" * 60)
    print("TEST 1: Creating schedule with custom settings")
    print("=" * 60)
    
    data = {
        "name": "Test Matematika",
        "day_of_week": 0,  # Monday
        "start_time": "09:00",
        "end_time": "10:30",
        "late_threshold_minutes": 15,
        "duplicate_check_minutes": 60
    }
    
    response = requests.post(f"{API_URL}/api/schedules", json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        result = response.json()
        schedule = result.get("schedule", {})
        
        # Verify settings were saved
        if schedule.get("late_threshold_minutes") == 15:
            print("✅ late_threshold_minutes saved correctly!")
        else:
            print(f"❌ late_threshold_minutes incorrect: {schedule.get('late_threshold_minutes')}")
        
        if schedule.get("duplicate_check_minutes") == 60:
            print("✅ duplicate_check_minutes saved correctly!")
        else:
            print(f"❌ duplicate_check_minutes incorrect: {schedule.get('duplicate_check_minutes')}")
        
        return schedule.get("id")
    else:
        print("❌ Failed to create schedule")
        return None

def test_update_schedule_settings(schedule_id):
    """Test updating schedule settings"""
    print("\n" + "=" * 60)
    print(f"TEST 2: Updating schedule {schedule_id} settings")
    print("=" * 60)
    
    data = {
        "late_threshold_minutes": 20,
        "duplicate_check_minutes": 90
    }
    
    response = requests.put(f"{API_URL}/api/schedules/{schedule_id}", json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 200:
        result = response.json()
        schedule = result.get("schedule", {})
        
        # Verify settings were updated
        if schedule.get("late_threshold_minutes") == 20:
            print("✅ late_threshold_minutes updated correctly!")
        else:
            print(f"❌ late_threshold_minutes incorrect: {schedule.get('late_threshold_minutes')}")
        
        if schedule.get("duplicate_check_minutes") == 90:
            print("✅ duplicate_check_minutes updated correctly!")
        else:
            print(f"❌ duplicate_check_minutes incorrect: {schedule.get('duplicate_check_minutes')}")
    else:
        print("❌ Failed to update schedule")

def test_create_schedule_without_settings():
    """Test creating schedule without custom settings (should use global)"""
    print("\n" + "=" * 60)
    print("TEST 3: Creating schedule WITHOUT custom settings")
    print("=" * 60)
    
    data = {
        "name": "Test Fizika",
        "day_of_week": 1,  # Tuesday
        "start_time": "11:00",
        "end_time": "12:30"
    }
    
    response = requests.post(f"{API_URL}/api/schedules", json=data)
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    
    if response.status_code == 201:
        result = response.json()
        schedule = result.get("schedule", {})
        
        # Verify settings are null (will use global)
        if schedule.get("late_threshold_minutes") is None:
            print("✅ late_threshold_minutes is null (will use global)")
        else:
            print(f"⚠️ late_threshold_minutes: {schedule.get('late_threshold_minutes')}")
        
        if schedule.get("duplicate_check_minutes") is None:
            print("✅ duplicate_check_minutes is null (will use global)")
        else:
            print(f"⚠️ duplicate_check_minutes: {schedule.get('duplicate_check_minutes')}")
    else:
        print("❌ Failed to create schedule")

if __name__ == "__main__":
    print("\n🧪 SCHEDULE SETTINGS API TEST\n")
    
    try:
        # Test 1: Create with settings
        schedule_id = test_create_schedule_with_settings()
        
        # Test 2: Update settings
        if schedule_id:
            test_update_schedule_settings(schedule_id)
        
        # Test 3: Create without settings
        test_create_schedule_without_settings()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server!")
        print("Make sure backend is running on http://localhost:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
