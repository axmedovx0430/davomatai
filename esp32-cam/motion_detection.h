#ifndef MOTION_DETECTION_H
#define MOTION_DETECTION_H

#include "esp_camera.h"

// Motion detection settings
#define MOTION_THRESHOLD 40      // Pixel intensity change threshold (0-255)
#define MOTION_PIXEL_COUNT 50    // Number of changed pixels to trigger motion

// Global variables for motion detection
camera_fb_t * prev_fb = NULL;

// Function to check for motion
// Returns true if motion detected, false otherwise
bool checkMotion(camera_fb_t * current_fb) {
    if (!current_fb) return false;
    
    // If no previous frame, save current as previous and return false
    if (!prev_fb) {
        prev_fb = (camera_fb_t*)malloc(sizeof(camera_fb_t));
        prev_fb->len = current_fb->len;
        prev_fb->width = current_fb->width;
        prev_fb->height = current_fb->height;
        prev_fb->format = current_fb->format;
        prev_fb->buf = (uint8_t*)malloc(current_fb->len);
        memcpy(prev_fb->buf, current_fb->buf, current_fb->len);
        return false;
    }
    
    // Compare frames
    int changed_pixels = 0;
    int len = current_fb->len;
    
    // Simple comparison: check every 4th byte (optimization)
    // Only works well for Grayscale or RGB565. For JPEG, we can't easily compare pixels directly without decoding.
    // BUT: Since we are switching resolutions, we can use GRAYSCALE for motion detection!
    
    for (int i = 0; i < len; i += 4) {
        if (abs(current_fb->buf[i] - prev_fb->buf[i]) > MOTION_THRESHOLD) {
            changed_pixels++;
        }
    }
    
    // Update previous frame
    if (prev_fb->len != current_fb->len) {
        free(prev_fb->buf);
        prev_fb->len = current_fb->len;
        prev_fb->buf = (uint8_t*)malloc(current_fb->len);
    }
    memcpy(prev_fb->buf, current_fb->buf, current_fb->len);
    
    return changed_pixels > MOTION_PIXEL_COUNT;
}

void cleanupMotion() {
    if (prev_fb) {
        if (prev_fb->buf) free(prev_fb->buf);
        free(prev_fb);
        prev_fb = NULL;
    }
}

#endif
