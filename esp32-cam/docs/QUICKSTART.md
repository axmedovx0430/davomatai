# Quick Start Guide

ESP32-CAM Davomat Tizimini tez ishga tushirish qo'llanmasi.

## 1. Talablar

- **Python 3.8+**
- **Node.js 18+**
- **PostgreSQL 12+**
- **Git**

## 2. Loyihani Yuklab Olish

```bash
git clone https://github.com/your-username/davomatai.git
cd davomatai
```

## 3. Avtomatik Sozlash

### Windows:
```powershell
.\setup.ps1
```

### Linux/Mac:
```bash
chmod +x setup.sh
./setup.sh
```

## 4. Database Yaratish

```bash
# PostgreSQL ga kirish
psql -U postgres

# Database yaratish
CREATE DATABASE attendance_db;
\q

# Schema yuklash
psql -U postgres -d attendance_db -f backend/database/schema.sql
```

## 5. Environment Variables

### Backend (.env)
```bash
cd backend
cp .env.example .env
# .env faylni tahrirlang
```

Kerakli o'zgarishlar:
- `DATABASE_URL` - PostgreSQL connection string
- `TELEGRAM_BOT_TOKEN` - BotFather dan olingan token
- `SECRET_KEY` - Random string

### Frontend (.env.local)
```bash
cd frontend
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
```

## 6. Dastlabki Ma'lumotlar

```bash
cd backend
source venv/bin/activate  # Linux/Mac
# yoki
.\venv\Scripts\Activate.ps1  # Windows

python init_db.py
```

Bu admin user va birinchi device yaratadi. API key ni saqlang!

## 7. Ishga Tushirish

### Terminal 1 - Backend:
```bash
cd backend
source venv/bin/activate  # Linux/Mac
python main.py
```

### Terminal 2 - Frontend:
```bash
cd frontend
npm run dev
```

## 8. Brauzerda Ochish

http://localhost:3000

## 9. ESP32-CAM Sozlash

1. `esp32-cam/config.h` ni tahrirlang:
```cpp
#define WIFI_SSID "YourWiFi"
#define WIFI_PASSWORD "YourPassword"
#define API_ENDPOINT "http://192.168.1.100:8000/api/face/upload"
#define API_KEY "device-api-key-from-init_db"
```

2. Arduino IDE da yuklang

## 10. Birinchi Foydalanuvchi Qo'shish

1. Admin panelda **Users** ga o'ting
2. **Yangi Foydalanuvchi** tugmasini bosing
3. Ma'lumotlarni to'ldiring
4. Yuz rasmini yuklang

## ✅ Tayyor!

ESP32-CAM yuzni taniydi va davomat yozadi.

## Muammolar?

- [Troubleshooting](docs/ESP32_SETUP.md#troubleshooting)
- [API Documentation](docs/API.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
