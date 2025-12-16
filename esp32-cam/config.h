/*
 * Configuration file for ESP32-CAM
 * 
 * IMPORTANT: Update these values before uploading!
 */

#ifndef CONFIG_H
#define CONFIG_H

// WiFi credentials
#define WIFI_SSID "laptop lenevo"
#define WIFI_PASSWORD "11111111"

// Backend API configuration
#define API_ENDPOINT "http://192.168.137.1:8080/api/face/upload"
#define API_KEY "kHBjHqVEi44yDZtPaDpSIkP8qwcrlMOGv4HxzKMuedw"

// Camera settings
#define CAMERA_MODEL_AI_THINKER  // ESP32-CAM board type

#endif
