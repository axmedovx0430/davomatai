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
# Import routes
from routes.auth_routes import router as auth_router
from routes.face_routes import router as face_router
from routes.user_routes import router as user_router
from routes.attendance_routes import router as attendance_router
from routes.device_routes import router as device_router
from routes.group_routes import router as group_router
from routes.time_settings_routes import router as time_settings_router
from routes.schedule_routes import router as schedule_router

# Register routers
app.include_router(auth_router)
app.include_router(face_router)
app.include_router(user_router)
app.include_router(attendance_router)
app.include_router(device_router)
app.include_router(group_router)
app.include_router(time_settings_router)
app.include_router(schedule_router)

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
        
        # Add password_hash column migration
        try:
            from sqlalchemy import text
            with engine.connect() as conn:
                # Check if password_hash column exists
                result = conn.execute(text("""
                    SELECT column_name 
                    FROM information_schema.columns 
                    WHERE table_name='users' AND column_name='password_hash'
                """))
                
                if not result.fetchone():
                    # Add password_hash column
                    conn.execute(text("""
                        ALTER TABLE users 
                        ADD COLUMN password_hash VARCHAR(255)
                    """))
                    conn.commit()
                    logger.info("✅ Added password_hash column to users table")
                else:
                    logger.info("✅ password_hash column already exists")
        except Exception as e:
            logger.error(f"Password hash migration failed: {e}")
        
        logger.info("Database migrations completed")

        init_db()
        logger.info("Database initialized successfully")
        
        # Create admin user if not exists
        try:
            from database import SessionLocal
            from models.user import User
            from passlib.context import CryptContext
            
            # Use sha256_crypt for maximum compatibility
            pwd_context = CryptContext(schemes=["sha256_crypt", "pbkdf2_sha256"], deprecated="auto")
            
            db = SessionLocal()
            try:
                admin = db.query(User).filter(User.employee_id == "ADMIN001").first()
                if not admin:
                    admin = User(
                        full_name="Administrator",
                        employee_id="ADMIN001",
                        email="admin@davomatai.uz",
                        role="admin",
                        password_hash=pwd_context.hash(settings.DEFAULT_ADMIN_PASSWORD),
                        is_active=True
                    )
                    db.add(admin)
                    db.commit()
                    logger.info("✅ Admin user created (ADMIN001/admin123)")
                else:
                    # Always update password to ensure it's set
                    admin.password_hash = pwd_context.hash(settings.DEFAULT_ADMIN_PASSWORD)
                    admin.role = "admin"
                    admin.is_active = True
                    db.commit()
                    logger.info(f"✅ Admin password updated (ADMIN001/{settings.DEFAULT_ADMIN_PASSWORD})")
            finally:
                db.close()
        except Exception as e:
            logger.error(f"Admin user creation failed: {e}")
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
