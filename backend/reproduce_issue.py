import requests
import json

API_URL = "http://localhost:8080/api/schedules/5"

def test_update(payload, description):
    print(f"--- Testing: {description} ---")
    try:
        response = requests.put(API_URL, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response Body: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

# Payload 1: Mimic successful request (baseline)
payload_valid = {
    "name": "Test Schedule",
    "day_of_week": 1,
    "start_time": "09:00",
    "end_time": "10:30",
    "group_id": 1
}
# test_update(payload_valid, "Valid Payload")

# Payload 2: Empty string for effective_from
payload_empty_date = {
    "name": "Test Schedule",
    "effective_from": ""
}
test_update(payload_empty_date, "Empty string for effective_from")

# Payload 3: Invalid time format
payload_invalid_time = {
    "name": "Test Schedule",
    "start_time": "9:00"
}
test_update(payload_invalid_time, "Invalid time format (9:00)")

# Payload 4: Empty string for start_time
payload_empty_time = {
    "name": "Test Schedule",
    "start_time": ""
}
test_update(payload_empty_time, "Empty string for start_time")
