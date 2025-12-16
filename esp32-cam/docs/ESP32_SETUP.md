# ESP32-CAM Setup Guide

ESP32-CAM AI-Thinker modulini sozlash va firmware yuklash qo'llanmasi.

## Kerakli Jihozlar

1. **ESP32-CAM** (AI-Thinker)
2. **FTDI Programmer** (USB to TTL) yoki **ESP32-CAM-MB** (USB adapter)
3. **Micro USB cable**
4. **Jumper wires** (agar FTDI ishlatilsa)
5. **5V Power supply** (2A tavsiya etiladi)

## Arduino IDE Sozlash

### 1. Arduino IDE O'rnatish

[Arduino IDE](https://www.arduino.cc/en/software) ni yuklab oling va o'rnating.

### 2. ESP32 Board Support Qo'shish

1. Arduino IDE ni oching
2. **File** → **Preferences**
3. **Additional Board Manager URLs** ga qo'shing:
   ```
   https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
   ```
4. **Tools** → **Board** → **Boards Manager**
5. "esp32" ni qidiring va **esp32 by Espressif Systems** ni o'rnating

### 3. Board Tanlash

1. **Tools** → **Board** → **ESP32 Arduino**
2. **AI Thinker ESP32-CAM** ni tanlang

### 4. Port Sozlamalari

- **Upload Speed**: 115200
- **Flash Frequency**: 80MHz
- **Flash Mode**: QIO
- **Partition Scheme**: Huge APP (3MB No OTA)
- **Core Debug Level**: None
- **Port**: COM port ni tanlang

## Hardware Ulanish

### FTDI Programmer Bilan

| FTDI | ESP32-CAM |
|------|-----------|
| GND  | GND       |
| 5V   | 5V        |
| RX   | U0T (TX)  |
| TX   | U0R (RX)  |

**Upload Mode uchun**:
- GPIO0 ni GND ga ulang (jumper wire)

**Normal Mode uchun**:
- GPIO0 ni GND dan ajrating

### ESP32-CAM-MB Bilan

ESP32-CAM ni to'g'ridan-to'g'ri MB adapterga joylashtiring va USB orqali ulang. Jumper kerak emas.

## Firmware Yuklash

### 1. Loyihani Ochish

1. Arduino IDE da **File** → **Open**
2. `esp32-cam/esp32-cam.ino` ni tanlang

### 2. Config.h Tahrirlash

`config.h` faylini oching va quyidagilarni to'ldiring:

```cpp
// WiFi credentials
#define WIFI_SSID "YourWiFiName"
#define WIFI_PASSWORD "YourWiFiPassword"

// Backend API configuration
#define API_ENDPOINT "http://192.168.1.100:8000/api/face/upload"
#define API_KEY "your-device-api-key-from-admin-panel"
```

**API Key olish**:
1. Admin panelni oching
2. **Devices** sahifasiga o'ting
3. **Yangi Qurilma** qo'shing
4. API Key ni nusxalang

### 3. Upload Qilish

1. ESP32-CAM ni upload mode ga o'tkazing:
   - FTDI: GPIO0 ni GND ga ulang
   - MB: BOOT tugmasini bosib turing
2. **Sketch** → **Upload** (yoki Ctrl+U)
3. Upload tugaguncha kuting (1-2 daqiqa)
4. Upload tugagach:
   - FTDI: GPIO0 ni GND dan ajrating
   - MB: RESET tugmasini bosing
5. Serial Monitor ni oching (115200 baud)

## Serial Monitor Chiqishi

Muvaffaqiyatli yuklanganda quyidagicha ko'rinadi:

```
ESP32-CAM Attendance System Starting...
Connecting to WiFi: YourWiFiName
.....
WiFi Connected!
IP Address: 192.168.1.50
Camera initialized successfully
System ready. Starting face detection...

--- Capturing image ---
Image captured: 640x480, size: 15234 bytes
HTTP Status: 200
Response: {"success":true,"recognized":true,...}
✓ Image sent successfully
```

## LED Indikatorlar

- **Yashil LED (GPIO 12)**: Muvaffaqiyat
  - 2 marta miltillaydi: Yuz tanildi, davomat yozildi
  - 3 marta miltillaydi: WiFi ulandi

- **Qizil LED (GPIO 13)**: Xatolik
  - 3 marta miltillaydi: Xatolik yuz berdi
  - Doimiy yoniq: WiFi yoki kamera xatosi

- **Flash LED (GPIO 4)**: Rasm olishda yonadi

## Troubleshooting

### Upload xatosi: "Failed to connect"

**Yechim**:
1. GPIO0 GND ga ulanganligini tekshiring
2. TX/RX to'g'ri ulanganligini tekshiring (RX→TX, TX→RX)
3. RESET tugmasini bosib, upload boshlanganda qo'yib yuboring
4. USB cable va power supply tekshiring

### WiFi ulanmayapti

**Yechim**:
1. WiFi SSID va password to'g'riligini tekshiring
2. 2.4GHz WiFi ishlatilayotganligini tekshiring (5GHz ishlamaydi)
3. WiFi signal kuchli ekanligini tekshiring
4. Serial Monitor da xatolarni ko'ring

### Kamera ishlamayapti

**Yechim**:
1. Kamera kabeli to'g'ri ulanganligini tekshiring
2. Kamera moduli ishlaydimi tekshiring
3. Power supply yetarli ekanligini tekshiring (5V 2A)
4. Serial Monitor da "Camera init failed" xatosini qidiring

### Backend ga ulanmayapti

**Yechim**:
1. Backend ishlab turganligini tekshiring
2. API_ENDPOINT to'g'riligini tekshiring
3. API_KEY to'g'riligini tekshiring
4. Firewall backend portini bloklayotganligini tekshiring
5. Serial Monitor da HTTP status code ni ko'ring

### Rasm sifati yomon

**Yechim**:
1. Yoritishni yaxshilang
2. Kamera lensini tozalang
3. `camera_utils.h` da JPEG quality ni o'zgartiring (10-63, past = yaxshi)
4. Frame size ni o'zgartiring (FRAMESIZE_VGA, FRAMESIZE_SVGA)

## Kamera Sozlamalari

`camera_utils.h` faylida quyidagi sozlamalarni o'zgartirish mumkin:

```cpp
// Frame size
config.frame_size = FRAMESIZE_VGA;  // 640x480
// FRAMESIZE_QVGA (320x240) - tezroq
// FRAMESIZE_SVGA (800x600) - sifatliroq

// JPEG quality
config.jpeg_quality = 10;  // 0-63, past = yaxshi sifat

// Brightness, contrast, saturation
s->set_brightness(s, 0);   // -2 to 2
s->set_contrast(s, 0);     // -2 to 2
s->set_saturation(s, 0);   // -2 to 2
```

## PlatformIO (Ixtiyoriy)

PlatformIO ishlatish uchun:

```bash
# PlatformIO CLI o'rnatish
pip install platformio

# Loyihani build qilish
cd esp32-cam
pio run

# Upload qilish
pio run --target upload

# Serial monitor
pio device monitor
```

## Qo'shimcha Maslahatlar

1. **Power Supply**: USB power yetarli bo'lmasligi mumkin, tashqi 5V 2A adapter ishlating
2. **Antenna**: WiFi signal zaif bo'lsa, tashqi antenna ulang
3. **Cooling**: Uzoq vaqt ishlasa, sovutish uchun radiator qo'shing
4. **Case**: ESP32-CAM uchun 3D printed case tavsiya etiladi
5. **Multiple Cameras**: Bir nechta ESP32-CAM ishlatish mumkin, har biri o'z API key ga ega

## Xavfsizlik

- ⚠️ API Key ni hech kimga ko'rsatmang
- ⚠️ WiFi password ni kodda qoldirmang (production uchun)
- ⚠️ HTTPS ishlatish tavsiya etiladi (production)

## Yangilash

Firmware yangilash uchun:
1. Yangi kodni yozing
2. Upload qilish jarayonini takrorlang
3. Serial Monitor orqali tekshiring

## Qo'llab-quvvatlash

Muammolar bo'lsa:
1. Serial Monitor chiqishini nusxalang
2. GitHub Issues da savol bering
3. Config va ulanish sxemasini tekshiring
