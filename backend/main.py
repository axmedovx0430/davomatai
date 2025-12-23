"""
FastAPI Main Application
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from config import settings
from database import init_db
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('backend.log')
    ]
)
logger = logging.getLogger(__name__)
logger.info("VERSION: 2.0.0 - ROBUST SETTINGS - MAIN")

# Create FastAPI app
app = FastAPI(
    title="ESP32-CAM Attendance System API",
    description="Face recognition based attendance system",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes
from routes import face_routes, user_routes, attendance_routes, device_routes, group_routes, time_settings_routes, schedule_routes, auth_routes

# Register routers
app.include_router(auth_routes.router)
app.include_router(face_routes.router)
app.include_router(user_routes.router)
app.include_router(attendance_routes.router)
app.include_router(device_routes.router)
app.include_router(group_routes.router)
app.include_router(time_settings_routes.router)
app.include_router(schedule_routes.router)

# Serve uploaded files
if os.path.exists(settings.UPLOAD_DIR):
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info("Starting ESP32-CAM Attendance System API")
    
    # Initialize database
    try:
        # Run migrations first
        from database import engine
        from utils.migrations import migrate_users_table, migrate_schedules_table
        
        logger.info("Running database migrations...")
        migrate_users_table(engine)
        migrate_schedules_table(engine)
        logger.info("Database migrations completed")

        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
    
    # Start Telegram bot
    try:
        from services.telegram_service import telegram_service
        import asyncio
        # Start polling or setup webhook
        asyncio.create_task(telegram_service.start_polling())
        
        # If on Hugging Face, set the webhook
        if getattr(settings, "SPACE_ID", None):
            asyncio.create_task(telegram_service.set_webhook())
            
        logger.info("Telegram bot startup initiated")
    except Exception as e:
        logger.error(f"Failed to start Telegram bot: {e}")
    
    # Services are initialized lazily when needed
    logger.info("Services configured for lazy loading")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("Shutting down ESP32-CAM Attendance System API")
    
    # Stop Telegram bot
    try:
        from services.telegram_service import telegram_service
        await telegram_service.stop_polling()
    except Exception as e:
        logger.error(f"Failed to stop Telegram bot: {e}")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ESP32-CAM Attendance System API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "face_recognition": "loaded"
    }


@app.post("/api/telegram/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates via Webhook"""
    try:
        from services.telegram_service import telegram_service
        data = await request.json()
        success = await telegram_service.process_update(data)
        return {"status": "ok" if success else "error"}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="trace"
    )
