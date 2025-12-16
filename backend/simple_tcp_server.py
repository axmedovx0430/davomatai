import socket

IP = '0.0.0.0'
PORT = 8080

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((IP, PORT))
        server_socket.listen(1)
        print(f"✅ Raw TCP Server listening on {IP}:{PORT}")
        print("Waiting for ESP32 to connect...")
        
        while True:
            client_socket, addr = server_socket.accept()
            print(f"🔗 Connection accepted from {addr}")
            
            client_socket.settimeout(10)
            
            try:
                # Read headers
                data = b""
                while b"\r\n\r\n" not in data:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    data += chunk
                
                if data:
                    print(f"📥 Received Headers ({len(data)} bytes)")
                    headers_str = data.decode('utf-8', errors='ignore')
                    print(headers_str)
                    
                    # Extract Content-Length
                    content_length = 0
                    for line in headers_str.split('\r\n'):
                        if 'Content-Length:' in line:
                            content_length = int(line.split(':')[1].strip())
                            break
                    
                    print(f"📏 Expecting Body: {content_length} bytes")
                    
                    # Read Body
                    body = b""
                    # Check if we already have some body in 'data'
                    header_end_idx = data.find(b"\r\n\r\n") + 4
                    if header_end_idx < len(data):
                        body = data[header_end_idx:]
                    
                    while len(body) < content_length:
                        chunk = client_socket.recv(4096)
                        if not chunk:
                            break
                        body += chunk
                        print(f"   Received chunk: {len(chunk)} bytes (Total: {len(body)}/{content_length})")
                    
                    print(f"✅ Full Body Received: {len(body)} bytes")
                    
                    # Send response
                    response = "HTTP/1.1 200 OK\r\nContent-Length: 2\r\n\r\nOK"
                    client_socket.send(response.encode())
                    print("📤 Sent OK response")
                else:
                    print("⚠️ Connected but received NO data")
            except Exception as e:
                print(f"❌ Error receiving data: {e}")
            finally:
                client_socket.close()
                print("🔌 Connection closed")
                print("Waiting for next connection...")
                
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        server_socket.close()

if __name__ == "__main__":
    start_server()
