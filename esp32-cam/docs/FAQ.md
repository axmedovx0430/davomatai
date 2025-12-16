# FAQ - Tez-tez So'raladigan Savollar

## Umumiy Savollar

### Q: Bu tizim qanday ishlaydi?
**A:** ESP32-CAM kamera yuzni aniqlaydi, rasmni backend ga yuboradi. Backend InsightFace yordamida yuzni taniydi va davomat yozadi. Telegram orqali real-time xabar yuboriladi.

### Q: Qancha xodim uchun ishlaydi?
**A:** Nazariy jihatdan cheksiz. Amalda 100-500 xodim uchun optimal. Katta tashkilotlar uchun database va server resurslarini oshirish kerak.

### Q: Yuz tanish qanchalik aniq?
**A:** InsightFace 99%+ aniqlikka ega. Threshold 0.5 da false positive juda kam.

### Q: Offline ishlaydi mi?
**A:** Yo'q, ESP32-CAM WiFi orqali backend ga ulanishi kerak. Local network da ishlashi mumkin.

---

## Texnik Savollar

### Q: Qanday database ishlatiladi?
**A:** PostgreSQL. MySQL yoki SQLite ham ishlatish mumkin, lekin PostgreSQL tavsiya etiladi.

### Q: InsightFace modeli qancha joy egallaydi?
**A:** buffalo_l model ~500MB. RAM da ~1GB kerak.

### Q: Bir nechta ESP32-CAM ishlatish mumkinmi?
**A:** Ha, har biri o'z API key ga ega bo'lishi kerak.

### Q: Mobile app iOS uchun bormi?
**A:** Hozircha yo'q, faqat Android. iOS rejada.

---

## ESP32-CAM Savollar

### Q: Qaysi ESP32-CAM board ishlaydi?
**A:** AI-Thinker ESP32-CAM. Boshqa variantlar ham ishlashi mumkin, lekin pin configuration o'zgartirish kerak.

### Q: Kamera sifati yomon, nima qilish kerak?
**A:** 
- Yoritishni yaxshilang
- Lensni tozalang
- `camera_utils.h` da JPEG quality ni kamaytiring (10-15)
- Frame size ni oshiring (SVGA)

### Q: WiFi ulanmayapti?
**A:**
- 2.4GHz WiFi ishlatilayotganligini tekshiring (5GHz ishlamaydi)
- SSID va password to'g'riligini tekshiring
- Signal kuchli ekanligini tekshiring

### Q: Power supply qancha bo'lishi kerak?
**A:** Kamida 5V 2A. USB power yetarli bo'lmasligi mumkin.

---

## Backend Savollar

### Q: Cloud hostingda qancha xarajat?
**A:** 
- Railway: $5-10/oy
- DigitalOcean: $6-12/oy
- Vercel (frontend): Bepul

### Q: Telegram bot majburiy mi?
**A:** Yo'q, ixtiyoriy. Bot tokensiz ham ishlaydi, faqat xabarlar yuborilmaydi.

### Q: API rate limiting bormi?
**A:** Hozircha yo'q. Production uchun qo'shish tavsiya etiladi.

---

## Frontend Savollar

### Q: Dark mode bormi?
**A:** Hozircha yo'q, rejada.

### Q: Mobile responsive mi?
**A:** Ha, Tailwind CSS responsive design.

### Q: Real-time updates qanday ishlaydi?
**A:** React Query auto-refresh (30s interval). WebSocket rejada.

---

## Xavfsizlik Savollar

### Q: API keylar qanday saqlanadi?
**A:** SHA-256 hash + salt bilan database da.

### Q: Yuz ma'lumotlari xavfsizmi?
**A:** Embeddings (512 float) saqlanadi, rasm emas. GDPR compliant.

### Q: HTTPS majburiy mi?
**A:** Production uchun ha, tavsiya etiladi.

---

## Muammolarni Hal Qilish

### Q: "Face not recognized" xatosi
**A:**
- Yoritish yaxshi ekanligini tekshiring
- Threshold ni pasaytiring (0.4 ga)
- Ko'proq yuz rasmlari qo'shing (turli burchaklar)

### Q: "Database connection failed"
**A:**
- PostgreSQL ishlab turganligini tekshiring
- DATABASE_URL to'g'riligini tekshiring
- Firewall portni bloklayotganligini tekshiring

### Q: Frontend backend ga ulanmayapti
**A:**
- CORS sozlamalarini tekshiring
- NEXT_PUBLIC_API_URL to'g'riligini tekshiring
- Backend ishlab turganligini tekshiring

---

## Kelajak Rejalar

### Q: Qanday yangi funksiyalar rejada?
**A:**
- WebSocket real-time
- Email notifications
- PDF reports
- Multi-language
- iOS app
- Face anti-spoofing

### Q: Open source mi?
**A:** Ha, MIT license.

---

## Qo'shimcha Yordam

Javob topolmadingizmi?
- [GitHub Issues](https://github.com/your-repo/issues)
- [Documentation](README.md)
- Email: support@example.com
