import requests
import socket

ip = "192.168.101.177"
port = 8000
url = f"http://{ip}:{port}/health"

print(f"Testing connection to {url}...")

try:
    # Test 1: Socket connect
    print(f"1. Testing TCP connection to {ip}:{port}...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex((ip, port))
    if result == 0:
        print("   SUCCESS: TCP Port is open and accepting connections.")
    else:
        print(f"   FAILURE: TCP Connect failed with error code {result}")
    sock.close()

    # Test 2: HTTP Request
    print(f"2. Testing HTTP GET request...")
    response = requests.get(url, timeout=2)
    print(f"   Status Code: {response.status_code}")
    print(f"   Response: {response.text}")

except Exception as e:
    print(f"   ERROR: {e}")
