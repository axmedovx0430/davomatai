# DavomatAI - Loyiha Dokumentatsiyasi

Bu hujjat **DavomatAI** loyihasining boshidan hozirgi kungacha bo'lgan barcha bosqichlarini, texnologik tarkibini va imkoniyatlarini o'z ichiga oladi.

---

## 🚀 Loyiha Haqida
**DavomatAI** — bu ESP32-CAM qurilmasi va sun'iy intellekt (Face Recognition) yordamida xodimlar yoki talabalar davomatini avtomatik hisobga olish tizimi. Tizim yuzni taniydi, vaqtni qayd etadi va barcha ma'lumotlarni Telegram bot hamda Web-panel orqali foydalanuvchilarga taqdim etadi.

---

## 🛠 Texnologiyalar (Tech Stack)

### Backend
- **FastAPI**: Yuqori tezlikdagi Python framework.
- **SQLAlchemy**: Ma'lumotlar bazasi bilan ishlash (ORM).
- **PostgreSQL/SQLite**: Ma'lumotlarni saqlash.
- **InsightFace**: Yuzni aniqlash va tanish uchun AI model.
- **OpenCV**: Tasvirlarga ishlov berish.
- **JWT (JSON Web Token)**: Xavfsiz autentifikatsiya.

### Frontend
- **Next.js 14**: Zamonaviy React framework.
- **Tailwind CSS**: Dizayn va stilizatsiya.
- **Lucide React**: Ikonkalar to'plami.

### Qurilma va Bot
- **ESP32-CAM**: Tasvirga oluvchi va serverga yuboruvchi mikrokontroller.
- **Python Telegram Bot**: Xabarnomalar va boshqaruv uchun.

---

## 🌟 Asosiy Imkoniyatlar

### 1. Yuz Tanish (Face Recognition)
- ESP32-CAM orqali olingan rasmlarni real-vaqtda tahlil qilish.
- Tizimga kiritilgan xodimlarni 99% aniqlikda tanish.
- Noma'lum shaxslar haqida ogohlantirish.

### 2. Davomatni Boshqarish
- Kelish va ketish vaqtlarini avtomatik qayd etish.
- Kechikishlarni hisoblash (Threshold tizimi).
- Kunlik, haftalik va oylik statistika.

### 3. Web Boshqaruv Paneli (Admin Panel)
- **Dashboard**: Real-vaqtda davomatni kuzatish.
- **Xodimlar boshqaruvi**: Yangi xodimlarni qo'shish, rasmlarini yuklash.
- **Guruhlar va Jadvallar**: Ish yoki dars jadvallarini sozlash.
- **Xavfsiz Login**: Faqat adminlar uchun JWT-ga asoslangan kirish tizimi.

### 4. Telegram Bot Integratsiyasi
- Har bir davomat qayd etilganda xodimga xabar yuborish.
- Adminlar uchun hisobotlar.
- Foydalanuvchi profili va shaxsiy statistika.

---

## 📈 Amalga Oshirilgan Ishlar (Milestones)

### 1-bosqich: Poydevor
- Backend arxitekturasi yaratildi.
- Ma'lumotlar bazasi sxemasi (Users, Attendance, Schedules, Groups) tuzildi.
- ESP32-CAM uchun API endpointlar tayyorlandi.

### 2-bosqich: AI Integratsiyasi
- InsightFace modeli backend-ga ulandi.
- Rasmlarni saqlash va ulardan embedding (raqamli belgi) olish tizimi yo'lga qo'yildi.
- Yuzni solishtirish algoritmi optimallashtirildi.

### 3-bosqich: Frontend va Dashboard
- Next.js-da zamonaviy va chiroyli interfeys yaratildi.
- Statistik grafiklar (Charts) qo'shildi.
- Live Feed (jonli efir) funksiyasi — oxirgi kelganlarni ko'rsatish.

### 4-bosqich: Xavfsizlik va Autentifikatsiya (Oxirgi yangilanish)
- **Mobile View** olib tashlandi va tizim professional Web-panelga aylantirildi.
- **JWT Authentication** tizimi joriy etildi.
- Parollarni xavfsiz saqlash (`pbkdf2_sha256`) yo'lga qo'yildi.
- **Protected Routes**: Avtorizatsiyadan o'tmagan foydalanuvchilar uchun dashboard yopildi.

---

## ⚙️ O'rnatish va Ishga Tushirish

### Backend
1. Kutubxonalarni o'rnatish: `pip install -r requirements.txt`
2. Ma'lumotlar bazasini sozlash: `python backend/main.py`
3. Admin yaratish: `python backend/create_admin.py`

### Frontend
1. `npm install`
2. `npm run dev`

---

## 🔒 Xavfsizlik Eslatmasi
- Barcha parollar xeshlangan holatda saqlanadi.
- JWT tokenlar 24 soat davomida amal qiladi.
- API kalitlari orqali qurilmalar autentifikatsiyasi ta'minlangan.

---
*Hujjat oxirgi marta 2024-yil 24-dekabrda yangilandi.*
