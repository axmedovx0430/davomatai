# API Documentation

ESP32-CAM Davomat Tizimi API qo'llanmasi.

## Base URL

```
http://localhost:8000
```

Production: `https://your-domain.com`

## Authentication

Barcha API so'rovlar `X-API-Key` header bilan himoyalangan.

```http
X-API-Key: your-api-key-here
```

### API Key Turlari

1. **Device API Key** - ESP32-CAM uchun
2. **User API Key** - Mobile app va admin panel uchun

---

## Face Recognition Endpoints

### Upload Face for Recognition

ESP32-CAM dan yuz rasmini yuklash va tanish.

**Endpoint**: `POST /api/face/upload`

**Headers**:
```http
Content-Type: multipart/form-data
X-API-Key: device-api-key
```

**Request Body**:
```
file: (binary) - JPEG image file
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Attendance recorded successfully",
  "recognized": true,
  "user": {
    "id": 1,
    "full_name": "John Doe",
    "employee_id": "EMP001",
    "email": "john@example.com",
    "phone": "+998901234567"
  },
  "confidence": 95.5,
  "attendance": {
    "id": 123,
    "check_in_time": "2025-11-29T09:15:30",
    "status": "present"
  },
  "duplicate": false
}
```

**Response** (Not Recognized):
```json
{
  "success": true,
  "message": "Face detected but not recognized",
  "recognized": false
}
```

---

### Register New Face

Foydalanuvchi uchun yangi yuz ro'yxatdan o'tkazish.

**Endpoint**: `POST /api/face/register?user_id={user_id}`

**Headers**:
```http
Content-Type: multipart/form-data
X-API-Key: admin-api-key
```

**Request Body**:
```
file: (binary) - JPEG image file
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Face registered successfully",
  "face": {
    "id": 5,
    "user_id": 1,
    "image_path": "/uploads/faces/EMP001_20251129_091530.jpg",
    "registered_at": "2025-11-29T09:15:30"
  }
}
```

---

### Delete Face

Yuzni o'chirish.

**Endpoint**: `DELETE /api/face/{face_id}`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Face deleted successfully"
}
```

---

### Get User Faces

Foydalanuvchining barcha yuzlarini olish.

**Endpoint**: `GET /api/face/user/{user_id}`

**Response** (200 OK):
```json
{
  "success": true,
  "faces": [
    {
      "id": 5,
      "user_id": 1,
      "image_path": "/uploads/faces/EMP001_20251129_091530.jpg",
      "registered_at": "2025-11-29T09:15:30"
    }
  ]
}
```

---

## User Management Endpoints

### Get All Users

**Endpoint**: `GET /api/users?skip=0&limit=100&is_active=true`

**Query Parameters**:
- `skip` (optional): Pagination offset
- `limit` (optional): Items per page
- `is_active` (optional): Filter by active status

**Response** (200 OK):
```json
{
  "success": true,
  "count": 10,
  "users": [
    {
      "id": 1,
      "full_name": "John Doe",
      "employee_id": "EMP001",
      "phone": "+998901234567",
      "email": "john@example.com",
      "role": "user",
      "is_active": true,
      "created_at": "2025-11-01T10:00:00",
      "updated_at": "2025-11-29T09:00:00",
      "face_count": 2
    }
  ]
}
```

---

### Get User by ID

**Endpoint**: `GET /api/users/{user_id}`

---

### Get User by Employee ID

**Endpoint**: `GET /api/users/employee/{employee_id}`

---

### Create User

**Endpoint**: `POST /api/users`

**Request Body**:
```json
{
  "full_name": "John Doe",
  "employee_id": "EMP001",
  "phone": "+998901234567",
  "email": "john@example.com",
  "role": "user"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "User created successfully",
  "user": { ... }
}
```

---

### Update User

**Endpoint**: `PUT /api/users/{user_id}`

**Request Body**:
```json
{
  "full_name": "John Smith",
  "phone": "+998901234567",
  "is_active": true
}
```

---

### Delete User

**Endpoint**: `DELETE /api/users/{user_id}`

Soft delete - `is_active` ni `false` ga o'rnatadi.

---

## Attendance Endpoints

### Get Attendance Records

**Endpoint**: `GET /api/attendance?start_date=2025-11-01&end_date=2025-11-30&user_id=1`

**Query Parameters**:
- `start_date` (optional): YYYY-MM-DD format
- `end_date` (optional): YYYY-MM-DD format
- `user_id` (optional): Filter by user
- `skip`, `limit`: Pagination

**Response** (200 OK):
```json
{
  "success": true,
  "total": 50,
  "count": 10,
  "attendance": [
    {
      "id": 123,
      "user_id": 1,
      "user_name": "John Doe",
      "employee_id": "EMP001",
      "device_id": 1,
      "device_name": "Main Entrance",
      "check_in_time": "2025-11-29T09:15:30",
      "confidence": 0.955,
      "status": "present"
    }
  ]
}
```

---

### Get Today's Attendance

**Endpoint**: `GET /api/attendance/today`

**Response** (200 OK):
```json
{
  "success": true,
  "date": "2025-11-29",
  "count": 15,
  "attendance": [ ... ]
}
```

---

### Get Attendance Statistics

**Endpoint**: `GET /api/attendance/stats`

**Response** (200 OK):
```json
{
  "success": true,
  "date": "2025-11-29",
  "stats": {
    "total_users": 50,
    "present": 40,
    "late": 5,
    "absent": 5,
    "attendance_rate": 90.0
  }
}
```

---

### Get User Attendance

**Endpoint**: `GET /api/attendance/user/{user_id}?start_date=2025-11-01&end_date=2025-11-30`

---

### Get User Statistics

**Endpoint**: `GET /api/attendance/user/{user_id}/stats?days=30`

**Response** (200 OK):
```json
{
  "success": true,
  "user_id": 1,
  "period_days": 30,
  "stats": {
    "total_days": 30,
    "present": 25,
    "late": 3,
    "absent": 2,
    "attendance_rate": 93.33
  }
}
```

---

## Device Management Endpoints

### Get All Devices

**Endpoint**: `GET /api/devices?is_active=true`

**Response** (200 OK):
```json
{
  "success": true,
  "count": 3,
  "devices": [
    {
      "id": 1,
      "device_name": "Main Entrance",
      "location": "Building A, Floor 1",
      "is_active": true,
      "last_seen": "2025-11-29T09:15:30",
      "created_at": "2025-11-01T10:00:00"
    }
  ]
}
```

---

### Create Device

**Endpoint**: `POST /api/devices`

**Request Body**:
```json
{
  "device_name": "Main Entrance",
  "location": "Building A, Floor 1"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "Device created successfully",
  "device": { ... },
  "api_key": "generated-api-key-shown-once"
}
```

⚠️ **API key faqat bir marta ko'rsatiladi!**

---

### Update Device

**Endpoint**: `PUT /api/devices/{device_id}`

---

### Delete Device

**Endpoint**: `DELETE /api/devices/{device_id}`

---

### Regenerate API Key

**Endpoint**: `POST /api/devices/{device_id}/regenerate-key`

**Response** (200 OK):
```json
{
  "success": true,
  "message": "API key regenerated successfully",
  "device": { ... },
  "api_key": "new-api-key-shown-once"
}
```

---

## Health Check

### Health Endpoint

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "database": "connected",
  "face_recognition": "loaded"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid image file"
}
```

### 401 Unauthorized
```json
{
  "detail": "API key required"
}
```

### 404 Not Found
```json
{
  "detail": "User not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Face recognition failed: ..."
}
```

---

## Rate Limiting

Hozircha rate limiting yo'q, lekin production uchun qo'shish tavsiya etiladi.

---

## CORS

CORS `ALLOWED_ORIGINS` environment variable orqali sozlanadi.

Default: `http://localhost:3000`

---

## WebSocket (Future)

Real-time updates uchun WebSocket qo'llab-quvvatlash rejalashtirilgan.
