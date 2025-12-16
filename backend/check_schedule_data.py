import requests
import json
from datetime import date, timedelta

API_URL = "http://localhost:8080/api/schedules"

def get_week_schedules():
    print("--- Fetching Week Schedules ---")
    try:
        # Get current week dates
        today = date.today()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        
        url = f"{API_URL}/week?start_date={start_of_week}&end_date={end_of_week}"
        print(f"URL: {url}")
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            schedules = data.get('schedules', {})
            for day, day_schedules in schedules.items():
                print(f"Day {day}:")
                for s in day_schedules:
                    print(f"  ID: {s['id']}, Name: {s['name']}, Time: {s['start_time']}-{s['end_time']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

def get_schedule_5():
    print("\n--- Fetching Schedule 5 ---")
    try:
        response = requests.get(f"{API_URL}/5")
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    get_week_schedules()
    get_schedule_5()
