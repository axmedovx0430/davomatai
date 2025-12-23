/*
 * ESP32-CAM Attendance System with Motion Detection
 * 
 * This firmware:
 * 1. Connects to WiFi
 * 2. Initializes camera
 * 3. Monitors for motion using low-res frames
 * 4. When motion detected -> Captures high-res image -> Sends to backend
 * 5. Shows LED feedback
 */

#include "Arduino.h"
#include "WiFi.h"
#include "esp_camera.h"
#include "esp_http_client.h"
#include "soc/soc.h"           // Disable brownout problems
#include "soc/rtc_cntl_reg.h"  // Disable brownout problems
#include "config.h"
#include "camera_utils.h"
#include "motion_detection.h"

// LED pins for ESP32-CAM (AI Thinker)
#define LED_FLASH 4      // Built-in Flash LED (High power)
#define LED_BUILTIN_RED 33 // Built-in Red LED (Back side, Active LOW)

// Timing
unsigned long lastMotionCheck = 0;
const unsigned long MOTION_CHECK_INTERVAL = 100; // Check every 100ms
const unsigned long COOLDOWN_PERIOD = 5000;      // 5 seconds cooldown after upload

bool cooldownActive = false;
unsigned long cooldownStartTime = 0;

// Prevent multiple simultaneous uploads
bool isSendingImage = false;

// Simple response parsing
bool recognizedFlag = false;
bool responseReceived = false;

// HTTP event handler
esp_err_t http_event_handler(esp_http_client_event_t *evt) {
    switch(evt->event_id) {
        case HTTP_EVENT_ON_DATA:
            if (!esp_http_client_is_chunked_response(evt->client)) {
                char* data = (char*)evt->data;
                for(int i = 0; i < evt->data_len - 16; i++) {
                    if(strncmp(&data[i], "\"recognized\":", 13) == 0) {
                        if(strncmp(&data[i+13], "true", 4) == 0) {
                            recognizedFlag = true;
                            responseReceived = true;
                        } else if(strncmp(&data[i+13], "false", 5) == 0) {
                            recognizedFlag = false;
                            responseReceived = true;
                        }
                        break;
                    }
                }
            }
            break;
        default:
            break;
    }
    return ESP_OK;
}

void setup() {
    WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // Disable brownout detector
    
    Serial.begin(115200);
    Serial.println("\n\nESP32-CAM Attendance System (Motion Detect) Starting...");
    
    // Initialize LEDs
    pinMode(LED_BUILTIN_RED, OUTPUT);
    
    // Setup PWM for Flash LED (Channel 4)
    ledcSetup(4, 5000, 8);
    ledcAttachPin(LED_FLASH, 4);
    ledcWrite(4, 0);
    digitalWrite(LED_BUILTIN_RED, HIGH); // OFF
    
    // Connect to WiFi
    Serial.print("Connecting to WiFi: ");
    Serial.println(WIFI_SSID);
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int wifiAttempts = 0;
    while (WiFi.status() != WL_CONNECTED && wifiAttempts < 20) {
        delay(500);
        Serial.print(".");
        wifiAttempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println("\nWiFi Connected!");
        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());
        WiFi.setSleep(false);
        
        // Blink Red LED
        for(int i = 0; i < 3; i++) {
            digitalWrite(LED_BUILTIN_RED, LOW); delay(100);
            digitalWrite(LED_BUILTIN_RED, HIGH); delay(100);
        }
    } else {
        Serial.println("\nWiFi Connection Failed!");
        while(1) { 
            digitalWrite(LED_BUILTIN_RED, LOW); delay(100);
            digitalWrite(LED_BUILTIN_RED, HIGH); delay(100);
        }
    }
    
    // Initialize camera (Default to Low Res for Motion Detection)
    if (initCamera()) {
        Serial.println("Camera initialized");
        // Set to grayscale and low res for motion detection
        sensor_t * s = esp_camera_sensor_get();
        s->set_framesize(s, FRAMESIZE_QQVGA); // 160x120
        s->set_pixformat(s, PIXFORMAT_GRAYSCALE);
    } else {
        Serial.println("Camera init failed!");
        while(1) { delay(1000); }
    }
    
    checkServerConnection();
    Serial.println("System ready. Waiting for motion...");
}

void loop() {
    // Cooldown check
    if (cooldownActive) {
        if (millis() - cooldownStartTime >= COOLDOWN_PERIOD) {
            cooldownActive = false;
            Serial.println("Cooldown ended. Monitoring motion...");
            // Reset to motion detection mode
            sensor_t * s = esp_camera_sensor_get();
            s->set_framesize(s, FRAMESIZE_QQVGA);
            s->set_pixformat(s, PIXFORMAT_GRAYSCALE);
        } else {
            delay(100);
            return;
        }
    }
    
    // Motion Check
    if (millis() - lastMotionCheck >= MOTION_CHECK_INTERVAL) {
        lastMotionCheck = millis();
        
        camera_fb_t * fb = esp_camera_fb_get();
        if (!fb) return;
        
        bool motion = checkMotion(fb);
        esp_camera_fb_return(fb);
        
        if (motion) {
            Serial.println("⚠️ Motion Detected! Capturing high-res image...");
            
            // Switch to High Res JPEG
            sensor_t * s = esp_camera_sensor_get();
            s->set_pixformat(s, PIXFORMAT_JPEG);
            s->set_framesize(s, FRAMESIZE_VGA); // 640x480
            s->set_quality(s, 10); // High quality
            
            // Allow sensor to adjust (skip a few frames)
            for(int i=0; i<2; i++) {
                fb = esp_camera_fb_get();
                if (fb) esp_camera_fb_return(fb);
            }
            
            // Capture for Upload
            fb = esp_camera_fb_get();
            if (fb) {
                // Flash LED (Increased brightness for visibility)
                ledcWrite(4, 128); delay(100); ledcWrite(4, 0);
                
                int result = sendImageToServer(fb);
                esp_camera_fb_return(fb);
                
                if (result == 1) {
                    Serial.println("✓ User Recognized");
                    blinkRecognized();
                } else if (result == 0) {
                    Serial.println("? Not Recognized");
                    blinkNotRecognized();
                } else {
                    blinkError();
                }
                
                // Start Cooldown
                cooldownActive = true;
                cooldownStartTime = millis();
            }
        }
    }
}

// ... (Keep sendImageToServer and blink functions same as before, just ensure ledcWrite uses channel 4)
// I will copy the helper functions here for completeness

int sendImageToServer(camera_fb_t * fb) {
    if (WiFi.status() != WL_CONNECTED) {
        Serial.println("⚠️ WiFi not connected! Attempting to reconnect...");
        WiFi.reconnect();
        int attempts = 0;
        while (WiFi.status() != WL_CONNECTED && attempts < 10) {
            delay(100);
            attempts++;
        }
        if (WiFi.status() != WL_CONNECTED) {
            Serial.println("❌ WiFi reconnection failed");
            return -1;
        } else {
            Serial.println("✅ WiFi reconnected!");
        }
    }
    
    recognizedFlag = false;
    responseReceived = false;
    
    static const char* boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW";
    const char* bodyStartPart2 = "\r\nContent-Disposition: form-data; name=\"file\"; filename=\"face.jpg\"\r\nContent-Type: image/jpeg\r\n\r\n";
    
    esp_http_client_config_t config = {};
    config.url = API_ENDPOINT;
    config.method = HTTP_METHOD_POST;
    config.event_handler = http_event_handler;
    config.timeout_ms = 30000; // Increased timeout for online upload
    config.buffer_size = 1024;
    config.skip_cert_common_name_check = true; // Skip SSL verification for HF
    
    esp_http_client_handle_t client = esp_http_client_init(&config);
    if (!client) {
        Serial.println("❌ Failed to initialize HTTP client");
        return -1;
    }
    
    char contentTypeHeader[100];
    snprintf(contentTypeHeader, sizeof(contentTypeHeader), "multipart/form-data; boundary=%s", boundary);
    esp_http_client_set_header(client, "Content-Type", contentTypeHeader);
    esp_http_client_set_header(client, "X-API-Key", API_KEY);
    esp_http_client_set_header(client, "User-Agent", "ESP32-CAM-Attendance/2.0");
    
    // Calculate total length
    int totalLen = 2 + strlen(boundary) + strlen(bodyStartPart2) + fb->len + 2 + 2 + strlen(boundary) + 4;
    
    esp_err_t err = esp_http_client_open(client, totalLen);
    if (err != ESP_OK) {
        Serial.printf("❌ Failed to open connection: %s\n", esp_err_to_name(err));
        esp_http_client_cleanup(client);
        return -1;
    }
    
    esp_http_client_write(client, "--", 2);
    esp_http_client_write(client, boundary, strlen(boundary));
    esp_http_client_write(client, bodyStartPart2, strlen(bodyStartPart2));
    
    const int chunkSize = 1024; // Increased chunk size
    for (int i = 0; i < fb->len; i += chunkSize) {
        int writeLen = min(chunkSize, (int)(fb->len - i));
        esp_http_client_write(client, (const char*)(fb->buf + i), writeLen);
    }
    
    esp_http_client_write(client, "\r\n--", 4);
    esp_http_client_write(client, boundary, strlen(boundary));
    esp_http_client_write(client, "--\r\n", 4);
    
    // Trigger read to parse response
    esp_err_t fetch_err = esp_http_client_fetch_headers(client);
    int statusCode = esp_http_client_get_status_code(client);
    
    if (fetch_err != ESP_OK) {
        Serial.printf("❌ HTTP Fetch failed: %s\n", esp_err_to_name(fetch_err));
    } else {
        Serial.printf("📡 Server Response: %d\n", statusCode);
        
        char buffer[256];
        int read_len = esp_http_client_read(client, buffer, sizeof(buffer) - 1);
        if (read_len > 0) {
            buffer[read_len] = 0;
            // Serial.println(buffer); // Debug response body
        }
    }
    
    int result = -1;
    if (statusCode == 200) {
        result = recognizedFlag ? 1 : 0;
    } else {
        Serial.printf("⚠️ Upload failed with status: %d\n", statusCode);
    }
    
    esp_http_client_cleanup(client);
    return result;
}

void blinkRecognized() {
    for(int i = 0; i < 3; i++) {
        ledcWrite(4, 200); delay(100); ledcWrite(4, 0); delay(100);
    }
}

void blinkNotRecognized() {
    for(int i = 0; i < 4; i++) {
        digitalWrite(LED_BUILTIN_RED, LOW); delay(100);
        digitalWrite(LED_BUILTIN_RED, HIGH); delay(100);
    }
}

void blinkError() {
    digitalWrite(LED_BUILTIN_RED, LOW); delay(1000);
    digitalWrite(LED_BUILTIN_RED, HIGH);
}

void checkServerConnection() {
    esp_http_client_config_t config = {};
    String healthUrl = String(API_ENDPOINT);
    healthUrl.replace("/api/face/upload", "/health");
    config.url = healthUrl.c_str();
    config.method = HTTP_METHOD_GET;
    config.skip_cert_common_name_check = true;
    config.timeout_ms = 10000;
    
    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_err_t err = esp_http_client_perform(client);
    
    if (err == ESP_OK) {
        int statusCode = esp_http_client_get_status_code(client);
        Serial.printf("📡 Backend Health Check: %d\n", statusCode);
    } else {
        Serial.printf("❌ Backend unreachable: %s\n", esp_err_to_name(err));
    }
    esp_http_client_cleanup(client);
}

