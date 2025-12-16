-- ESP32-CAM Face Recognition Attendance System
-- Database Schema

-- Users table: tizim foydalanuvchilari
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    employee_id VARCHAR(50) UNIQUE NOT NULL,
    phone VARCHAR(20),
    email VARCHAR(255),
    role VARCHAR(20) DEFAULT 'user', -- 'admin' or 'user'
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Devices: ESP32-CAM qurilmalari
CREATE TABLE devices (
    id SERIAL PRIMARY KEY,
    device_name VARCHAR(100) NOT NULL,
    api_key VARCHAR(255) UNIQUE NOT NULL,
    location VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    last_seen TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Face embeddings: har bir foydalanuvchi uchun yuz embeddinglari
CREATE TABLE faces (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    embedding BYTEA NOT NULL, -- numpy array as bytes
    image_path VARCHAR(500),
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Attendance records: davomat yozuvlari
CREATE TABLE attendance (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    device_id INTEGER REFERENCES devices(id),
    check_in_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    confidence FLOAT,
    image_path VARCHAR(500),
    status VARCHAR(20) DEFAULT 'present' -- 'present', 'late', 'absent'
);

-- API keys: admin va mobile app uchun
CREATE TABLE api_keys (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    key_hash VARCHAR(255) UNIQUE NOT NULL,
    description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP
);

-- Indexes for performance
CREATE INDEX idx_attendance_user_date ON attendance(user_id, check_in_time);
CREATE INDEX idx_faces_user ON faces(user_id);
CREATE INDEX idx_users_employee_id ON users(employee_id);
CREATE INDEX idx_devices_api_key ON devices(api_key);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
