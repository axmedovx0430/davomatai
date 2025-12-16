# ESP32-CAM Davomat Tizimi

Yuz tanish (face recognition) asosida avtomatik davomat tizimi. ESP32-CAM kamera moduli, FastAPI backend, Next.js admin panel, Telegram bot va Flutter mobile ilovadan iborat.

## 🎯 Loyiha Haqida

Bu tizim ESP32-CAM OV2640 kamera yordamida xodimlarning yuzini taniydi va avtomatik ravishda davomat yozadi. Barcha ma'lumotlar PostgreSQL bazasida saqlanadi va real-time Telegram xabarlari yuboriladi.

## 🏗️ Arxitektura

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│  ESP32-CAM  │─────▶│   Backend    │─────▶│  PostgreSQL │
│   (OV2640)  │      │   (FastAPI)  │      │  Database   │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ├─────▶ Telegram Bot
                            │
                            ├─────▶ Next.js Admin Panel
                            │
                            └─────▶ Flutter Mobile App
```

## 📦 Komponentlar

### 1. Backend (FastAPI + PostgreSQL + InsightFace)
- **Face Recognition**: InsightFace (buffalo_l model)
- **Database**: PostgreSQL
- **API**: RESTful API
- **Telegram**: Real-time xabarlar

### 2. Frontend (Next.js 14)
- **Dashboard**: Real-time statistika
- **User Management**: Foydalanuvchilar boshqaruvi
- **Attendance**: Davomat tarixi va hisobotlar
- **Devices**: ESP32-CAM qurilmalar monitoring

### 3. ESP32-CAM Firmware
- **Camera**: OV2640 (VGA 640x480)
- **WiFi**: Avtomatik ulanish
- **LED Feedback**: Muvaffaqiyat/xatolik ko'rsatkichlari

### 4. Mobile App (Flutter - Android)
- **Profile**: Foydalanuvchi profili
- **Stats**: Davomat statistikasi
- **History**: Davomat tarixi

### 5. Telegram Bot
- **Notifications**: Real-time davomat xabarlari
- **Commands**: `/stats`, `/today`, `/help`

## 🚀 O'rnatish

### Backend

```bash
cd backend

# Virtual environment yaratish
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Dependencies o'rnatish
pip install -r requirements.txt

# .env fayl yaratish
copy .env.example .env
# .env faylni to'ldiring

# Database yaratish (PostgreSQL)
# psql -U postgres
# CREATE DATABASE attendance_db;

# Database schema yuklash
psql -U postgres -d attendance_db -f database/schema.sql

# Serverni ishga tushirish
python main.py
```

Backend `http://localhost:8000` da ishga tushadi.

### Frontend

```bash
cd frontend

# Dependencies o'rnatish
npm install

# .env.local yaratish
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Development server
npm run dev

# Production build
npm run build
npm start
```

Frontend `http://localhost:3000` da ochiladi.

### ESP32-CAM

1. **Arduino IDE** yoki **PlatformIO** o'rnating
2. ESP32 board support qo'shing
3. `esp32-cam/config.h` faylini tahrirlang:
   ```cpp
   #define WIFI_SSID "YourWiFiName"
   #define WIFI_PASSWORD "YourPassword"
   #define API_ENDPOINT "http://your-backend-url/api/face/upload"
   #define API_KEY "your-device-api-key"
   ```
4. `esp32-cam.ino` faylni yuklang
5. Serial Monitor orqali tekshiring (115200 baud)

### Mobile App

```bash
cd mobile

# Dependencies o'rnatish
flutter pub get

# API URL o'zgartirish
# lib/services/api_service.dart faylida baseUrl ni o'zgartiring

# Android build
flutter build apk --release

# APK fayl: build/app/outputs/flutter-apk/app-release.apk
```

## 📝 Foydalanish

### 1. Birinchi Sozlash

1. **Backend ishga tushiring**
2. **Admin panelni oching** (`http://localhost:3000`)
3. **Qurilma qo'shing**: Devices sahifasida yangi ESP32-CAM qo'shing, API key oling
4. **Foydalanuvchi qo'shing**: Users sahifasida yangi xodim qo'shing
5. **Yuz ro'yxatdan o'tkazing**: Foydalanuvchi uchun yuz rasmini yuklang

### 2. ESP32-CAM Sozlash

1. API key ni `config.h` ga kiriting
2. WiFi ma'lumotlarini kiriting
3. Backend URL ni kiriting
4. Firmware yuklang
5. Serial Monitor orqali tekshiring

### 3. Davomat Jarayoni

1. ESP32-CAM har 5 soniyada rasm oladi
2. Yuz aniqlansa, backend ga yuboriladi
3. Backend yuzni taniydi
4. Davomat yoziladi
5. Telegram xabar yuboriladi
6. LED muvaffaqiyatni ko'rsatadi (yashil)

## 🔧 Konfiguratsiya

### Backend Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/attendance_db
SECRET_KEY=your-secret-key
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_ADMIN_CHAT_IDS=123456789,987654321
INSIGHTFACE_MODEL=buffalo_l
FACE_MATCH_THRESHOLD=0.5
```

### Frontend Environment Variables

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 API Endpoints

### Face Recognition
- `POST /api/face/upload` - ESP32-CAM dan rasm yuklash
- `POST /api/face/register` - Yangi yuz ro'yxatdan o'tkazish
- `DELETE /api/face/{id}` - Yuzni o'chirish

### Users
- `GET /api/users` - Barcha foydalanuvchilar
- `POST /api/users` - Yangi foydalanuvchi
- `PUT /api/users/{id}` - Foydalanuvchini yangilash
- `DELETE /api/users/{id}` - Foydalanuvchini o'chirish

### Attendance
- `GET /api/attendance` - Davomat ro'yxati
- `GET /api/attendance/today` - Bugungi davomat
- `GET /api/attendance/stats` - Statistika

### Devices
- `GET /api/devices` - Qurilmalar ro'yxati
- `POST /api/devices` - Yangi qurilma
- `POST /api/devices/{id}/regenerate-key` - API key yangilash

## 🔐 Xavfsizlik

- **API Keys**: Barcha so'rovlar API key bilan himoyalangan
- **Device Authentication**: Har bir ESP32-CAM o'z API key ga ega
- **User API Keys**: Mobile app uchun alohida API keys
- **Password Hashing**: API keylar hash qilingan holda saqlanadi

## 🐛 Muammolarni Hal Qilish

### ESP32-CAM ulanmayapti
- WiFi ma'lumotlarini tekshiring
- Serial Monitor orqali xatolarni ko'ring
- Power supply yetarli ekanligini tekshiring (5V 2A)

### Yuz tanilmayapti
- Yoritish yaxshi ekanligini tekshiring
- Kamera to'g'ri yo'naltirilganligini tekshiring
- Face match threshold ni sozlang (0.4-0.6)

### Backend xatolari
- Database ulanishini tekshiring
- InsightFace model yuklanganligini tekshiring
- Log fayllarni ko'ring

## 📱 Telegram Bot Buyruqlari

- `/start` - Botni ishga tushirish
- `/stats` - Bugungi statistika
- `/today` - Bugungi davomat ro'yxati
- `/help` - Yordam

## 🌐 Cloud Deployment

Backend va frontend ni cloud hostingga joylashtirish uchun `docs/DEPLOYMENT.md` faylga qarang.

## 📄 Litsenziya

MIT License

## 👨‍💻 Muallif

ESP32-CAM Face Recognition Attendance System

## 🙏 Minnatdorchilik

- **InsightFace** - Face recognition model
- **FastAPI** - Backend framework
- **Next.js** - Frontend framework
- **Flutter** - Mobile app framework
