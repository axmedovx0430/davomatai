"""
Telegram Bot Service - User-focused features
"""
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import settings
import logging
from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user import User
from models.attendance import Attendance
from models.schedule import Schedule
from sqlalchemy import func, and_
import asyncio
from services.telegram_strings import STRINGS

logger = logging.getLogger(__name__)
logger.info("VERSION: 2.0.2 - STABLE - TELEGRAM")


class TelegramService:
    def __init__(self):
        self.bot: Optional[Bot] = None
        self.application: Optional[Application] = None
        self.user_states = {}  # Track user registration states
        self._initialize()
    
    def _initialize(self):
        """Initialize Telegram bot"""
        try:
            from telegram.request import HTTPXRequest
            
            # Safely get settings with defaults if missing
            logger.info(f"DEBUG: telegram_service _initialize. settings type: {type(settings)}")
            
            proxy_url = getattr(settings, "TELEGRAM_PROXY_URL", None)
            base_url = getattr(settings, "TELEGRAM_API_BASE_URL", "https://api.telegram.org/bot")
            token = getattr(settings, "TELEGRAM_BOT_TOKEN", None)
            
            if not token:
                logger.error("TELEGRAM_BOT_TOKEN is missing in settings!")
                return

            # Increase timeout for Hugging Face environment
            request = HTTPXRequest(
                connect_timeout=30, 
                read_timeout=30, 
                write_timeout=30, 
                pool_timeout=30,
                proxy_url=proxy_url
            )
            
            # Use custom base_url if provided (for mirrors)
            if base_url and not base_url.endswith("/"):
                base_url += "/"
                
            logger.info(f"Initializing bot with base_url: {base_url}")
            self.application = Application.builder().token(token).request(request).base_url(base_url).build()
            self.bot = self.application.bot
            
            # Register command handlers
            self.application.add_handler(CommandHandler("start", self.cmd_start))
            self.application.add_handler(CommandHandler("mystats", self.cmd_mystats))
            self.application.add_handler(CommandHandler("today", self.cmd_today))
            self.application.add_handler(CommandHandler("week", self.cmd_week))
            self.application.add_handler(CommandHandler("profile", self.cmd_profile))
            self.application.add_handler(CommandHandler("schedule", self.cmd_schedule))
            self.application.add_handler(CommandHandler("notify", self.cmd_notify))
            self.application.add_handler(CommandHandler("help", self.cmd_help))
            self.application.add_handler(CommandHandler("url", self.cmd_url))
            self.application.add_handler(CommandHandler("language", self.cmd_language))
            
            # Callback query handler for language selection
            self.application.add_handler(CallbackQueryHandler(self.handle_callback))
            
            # Message handler for registration
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
            
            logger.info("Telegram bot initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Telegram bot: {e}")
    
    async def send_message(self, chat_id: int, text: str, parse_mode: str = "HTML"):
        """Send message to specific chat"""
        try:
            await self.bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode)
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
    
    async def send_to_admins(self, text: str, parse_mode: str = "HTML"):
        """Send message to all admin chats"""
        for chat_id in settings.admin_chat_ids:
            await self.send_message(chat_id, text, parse_mode)
    
    def get_user_by_chat_id(self, chat_id: str) -> Optional[User]:
        """Get user by telegram chat ID"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.telegram_chat_id == str(chat_id)).first()
        finally:
            db.close()
    
    def get_user_by_employee_id(self, employee_id: str) -> Optional[User]:
        """Get user by employee ID"""
        db = SessionLocal()
        try:
            return db.query(User).filter(User.employee_id == employee_id).first()
        finally:
            db.close()
    
    def get_text(self, user: Optional[User], key: str, **kwargs) -> str:
        """Get localized text for user"""
        lang = user.language if user and user.language in STRINGS else "uz"
        text = STRINGS[lang].get(key, STRINGS["uz"].get(key, key))
        return text.format(**kwargs) if kwargs else text
    
    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command - Registration"""
        chat_id = str(update.effective_chat.id)
        user = self.get_user_by_chat_id(chat_id)
        
        if user:
            # Already registered
            message = self.get_text(user, "welcome_registered", name=user.full_name)
            message += self.get_text(user, "commands_list")
        else:
            # Start registration
            self.user_states[chat_id] = "awaiting_employee_id"
            message = self.get_text(None, "welcome_new")
        
        # Create Web App button
        webapp_button = InlineKeyboardButton(
            text=self.get_text(user, "open_app"), 
            web_app=WebAppInfo(url=f"{settings.frontend_url}/mobile")
        )
        keyboard = InlineKeyboardMarkup([[webapp_button]])
        
        await update.message.reply_text(message, parse_mode="HTML", reply_markup=keyboard)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages (for registration)"""
        chat_id = str(update.effective_chat.id)
        text = update.message.text.strip()
        
        if chat_id in self.user_states and self.user_states[chat_id] == "awaiting_employee_id":
            # Process employee ID
            db = SessionLocal()
            try:
                # Fetch user within the active session to avoid detachment
                db_user = db.query(User).filter(User.employee_id == text).first()
                if db_user:
                    db_user.telegram_chat_id = chat_id
                    db_user.telegram_username = update.effective_user.username
                    db_user.telegram_notifications = True
                    db_user.telegram_registered_at = datetime.now()
                    db.commit()
                    
                    if chat_id in self.user_states:
                        del self.user_states[chat_id]
                    
                    message = self.get_text(db_user, "reg_success", name=db_user.full_name, id=db_user.employee_id)
                    message += self.get_text(db_user, "commands_list")
                    
                    # Create Web App button for success message
                    webapp_button = InlineKeyboardButton(
                        text=self.get_text(db_user, "open_app"), 
                        web_app=WebAppInfo(url=f"{settings.frontend_url}/mobile")
                    )
                    keyboard = InlineKeyboardMarkup([[webapp_button]])
                    
                    await update.message.reply_text(message, parse_mode="HTML", reply_markup=keyboard)
                    return
                else:
                    message = self.get_text(None, "user_not_found", id=text)
                    await update.message.reply_text(message, parse_mode="HTML")
            except Exception as e:
                logger.error(f"Registration error: {e}")
                await update.message.reply_text(self.get_text(None, "error_occurred"), parse_mode="HTML")
            finally:
                db.close()
        else:
            # Fallback for unknown messages
            user = self.get_user_by_chat_id(chat_id)
            if user:
                await update.message.reply_text(
                    self.get_text(user, "unknown_cmd"),
                    parse_mode="HTML"
                )
            else:
                await update.message.reply_text(
                    self.get_text(None, "not_registered"),
                    parse_mode="HTML"
                )
    
    async def cmd_url(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Debug command to see current URLs"""
        message = f"""🌐 <b>Tizim manzillari:</b>

Frontend: <code>{settings.frontend_url}</code>
Webhook: <code>{settings.telegram_webhook_url}</code>
API Base: <code>{settings.TELEGRAM_API_BASE_URL}</code>"""
        await update.message.reply_text(message, parse_mode="HTML")

    async def cmd_mystats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /mystats command - Personal statistics"""
        chat_id = str(update.effective_chat.id)
        db = SessionLocal()
        try:
            # Fetch user within session
            db_user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not db_user:
                await update.message.reply_text(
                    "❌ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini bosing.",
                    parse_mode="HTML"
                )
                return

            # Get current month stats
            now = datetime.now()
            month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            
            total_attendance = db.query(Attendance).filter(
                and_(
                    Attendance.user_id == db_user.id,
                    Attendance.check_in_time >= month_start
                )
            ).count()
            
            present_count = db.query(Attendance).filter(
                and_(
                    Attendance.user_id == db_user.id,
                    Attendance.check_in_time >= month_start,
                    Attendance.status == "present"
                )
            ).count()
            
            late_count = db.query(Attendance).filter(
                and_(
                    Attendance.user_id == db_user.id,
                    Attendance.check_in_time >= month_start,
                    Attendance.status == "late"
                )
            ).count()
            
            # Get all-time stats
            total_all_time = db.query(Attendance).filter(Attendance.user_id == db_user.id).count()
            
            attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
            
            message = self.get_text(
                db_user, "stats_title", 
                month=now.strftime('%B %Y'), 
                present=present_count, 
                late=late_count, 
                rate=attendance_rate, 
                year=now.year, 
                total=total_all_time
            )
            
        except Exception as e:
            logger.error(f"Stats error: {e}")
            message = self.get_text(None, "error_occurred")
        finally:
            db.close()
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_today(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /today command - Today's attendance"""
        chat_id = str(update.effective_chat.id)
        db = SessionLocal()
        try:
            # Fetch user within session
            db_user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not db_user:
                await update.message.reply_text(
                    "❌ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini bosing.",
                    parse_mode="HTML"
                )
                return

            today = datetime.now().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            attendances = db.query(Attendance).filter(
                and_(
                    Attendance.user_id == db_user.id,
                    Attendance.check_in_time >= today_start,
                    Attendance.check_in_time <= today_end
                )
            ).order_by(Attendance.check_in_time).all()
            
            if attendances:
                message = self.get_text(db_user, "today_title", date=today.strftime('%d %B'))
                
                for i, att in enumerate(attendances, 1):
                    status_emoji = "✅" if att.status == "present" else "⏰"
                    time_str = att.check_in_time.strftime("%H:%M")
                    schedule_name = att.schedule.name if att.schedule else "Noma'lum"
                    message += f"{i}. {status_emoji} {time_str} - {schedule_name}\n"
                
                present = sum(1 for a in attendances if a.status == "present")
                total = len(attendances)
                message += f"\nBugun: {present}/{total} ({present/total*100:.0f}%)"
            else:
                message = self.get_text(db_user, "no_attendance_today", date=today.strftime('%d %B'))
            
        except Exception as e:
            logger.error(f"Today error: {e}")
            message = self.get_text(None, "error_occurred")
        finally:
            db.close()
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_week(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /week command - Weekly report"""
        await update.message.reply_text(
            "📅 Haftalik hisobot funksiyasi tez orada qo'shiladi...",
            parse_mode="HTML"
        )
    
    async def cmd_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /profile command - User profile"""
        chat_id = str(update.effective_chat.id)
        db = SessionLocal()
        try:
            # Fetch user within session
            db_user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not db_user:
                await update.message.reply_text(
                    "❌ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini bosing.",
                    parse_mode="HTML"
                )
                return

            total_attendance = db.query(Attendance).filter(Attendance.user_id == db_user.id).count()
            present_count = db.query(Attendance).filter(
                and_(Attendance.user_id == db_user.id, Attendance.status == "present")
            ).count()
            late_count = db.query(Attendance).filter(
                and_(Attendance.user_id == db_user.id, Attendance.status == "late")
            ).count()
            
            attendance_rate = (present_count / total_attendance * 100) if total_attendance > 0 else 0
            
            email = db_user.email or "Yo'q"
            groups_str = ", ".join([g.name for g in db_user.groups]) if db_user.groups else "Yo'q"
            
            message = self.get_text(
                db_user, "profile_title",
                name=db_user.full_name,
                id=db_user.employee_id,
                phone=phone,
                email=email,
                groups=groups_str,
                rate=attendance_rate,
                total=total_attendance,
                present=present_count,
                late=late_count
            )
        except Exception as e:
            logger.error(f"Profile error: {e}")
            message = self.get_text(None, "error_occurred")
        finally:
            db.close()
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_schedule(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /schedule command - Today's schedule"""
        await update.message.reply_text(
            "📅 Jadval funksiyasi tez orada qo'shiladi...",
            parse_mode="HTML"
        )
    
    async def cmd_notify(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /notify command - Toggle notifications"""
        chat_id = str(update.effective_chat.id)
        db = SessionLocal()
        try:
            # Fetch user within session
            db_user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
            if not db_user:
                await update.message.reply_text(
                    "❌ Siz ro'yxatdan o'tmagansiz. /start buyrug'ini bosing.",
                    parse_mode="HTML"
                )
                return

            db_user.telegram_notifications = not db_user.telegram_notifications
            db.commit()
            
            if db_user.telegram_notifications:
                message = self.get_text(db_user, "notify_on")
            else:
                message = self.get_text(db_user, "notify_off")
        except Exception as e:
            logger.error(f"Notify toggle error: {e}")
            message = self.get_text(None, "error_occurred")
        finally:
            db.close()
        
        await update.message.reply_text(message, parse_mode="HTML")
    
    async def cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        chat_id = str(update.effective_chat.id)
        user = self.get_user_by_chat_id(chat_id)
        help_message = self.get_text(user, "help_text")
        await update.message.reply_text(help_message, parse_mode="HTML")
    
    async def cmd_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /language command"""
        chat_id = str(update.effective_chat.id)
        user = self.get_user_by_chat_id(chat_id)
        
        keyboard = [
            [
                InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data="lang_uz"),
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            self.get_text(user, "lang_select"),
            reply_markup=reply_markup,
            parse_mode="HTML"
        )

    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries (language selection)"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        chat_id = str(update.effective_chat.id)
        
        if data.startswith("lang_"):
            new_lang = data.split("_")[1]
            db = SessionLocal()
            try:
                db_user = db.query(User).filter(User.telegram_chat_id == chat_id).first()
                if db_user:
                    db_user.language = new_lang
                    db.commit()
                    
                    await query.edit_message_text(
                        self.get_text(db_user, "lang_updated"),
                        parse_mode="HTML"
                    )
                    
                    # Send welcome message in new language
                    message = self.get_text(db_user, "welcome_registered", name=db_user.full_name)
                    message += self.get_text(db_user, "commands_list")
                    
                    webapp_button = InlineKeyboardButton(
                        text=self.get_text(db_user, "open_app"), 
                        web_app=WebAppInfo(url=f"{settings.frontend_url}/mobile")
                    )
                    keyboard = InlineKeyboardMarkup([[webapp_button]])
                    
                    await context.bot.send_message(
                        chat_id=int(chat_id),
                        text=message,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
            except Exception as e:
                logger.error(f"Language update error: {e}")
            finally:
                db.close()
    
    async def notify_attendance(self, user_name: str, employee_id: str, check_in_time: str, confidence: float, status: str):
        """Send attendance notification to admin chats"""
        try:
            status_emoji = "✅" if status == "present" else "⏰"
            status_text = "Keldi" if status == "present" else "Kechikdi"
            
            message = f"""{status_emoji} <b>Davomat</b>

👤 {user_name}
🆔 <code>{employee_id}</code>
🕐 {check_in_time}
📍 {status_text}
🎯 Ishonch: {confidence:.1f}%"""
            
            await self.send_to_admins(message)
            
        except Exception as e:
            logger.error(f"Admin notification error: {e}")
    
    async def notify_user_attendance(self, user_id: int, schedule_name: str, check_in_time: str, status: str, late_minutes: int = 0):
        """Send personal attendance notification to user"""
        db = SessionLocal()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user or not user.telegram_chat_id or not user.telegram_notifications:
                return
            
            status_emoji = "✅" if status == "present" else "⏰"
            status_text = "Keldingiz" if status == "present" else f"Kechikdingiz ({late_minutes} daqiqa)"
            
            # Get today's attendance count
            today = datetime.now().date()
            today_start = datetime.combine(today, datetime.min.time())
            today_end = datetime.combine(today, datetime.max.time())
            
            today_count = db.query(Attendance).filter(
                and_(
                    Attendance.user_id == user_id,
                    Attendance.check_in_time >= today_start,
                    Attendance.check_in_time <= today_end
                )
            ).count()
            
            message = f"""{status_emoji} <b>Davomat qabul qilindi!</b>

👤 {user.full_name}
📚 {schedule_name}
🕐 {check_in_time}
📍 {status_text}

Bugun: {today_count} ta davomat"""
            
            await self.send_message(int(user.telegram_chat_id), message)
            
        except Exception as e:
            logger.error(f"User notification error: {e}")
        finally:
            db.close()
    
    async def process_update(self, data: dict):
        """Process update received via webhook"""
        try:
            update = Update.de_json(data, self.bot)
            await self.application.update_queue.put(update)
            return True
        except Exception as e:
            logger.error(f"Failed to process webhook update: {e}")
            return False

    async def set_webhook(self):
        """Set telegram webhook"""
        webhook_url = settings.telegram_webhook_url
        if not webhook_url:
            logger.warning("No webhook URL configured, skipping set_webhook")
            return False
            
        try:
            # Wait a bit for server to be ready
            await asyncio.sleep(5)
            await self.bot.set_webhook(url=webhook_url)
            logger.info(f"Telegram webhook set successfully to: {webhook_url}")
            return True
        except Exception as e:
            logger.error(f"Failed to set telegram webhook: {e}")
            return False

    async def start_polling(self):
        """Start bot polling (for standalone mode) or setup webhook if on HF"""
        # If on Hugging Face, we use webhooks instead of polling
        space_id = getattr(settings, "SPACE_ID", None)
        if space_id:
            logger.info(f"Hugging Face environment detected. SPACE_ID: {space_id}")
            await self.application.initialize()
            await self.application.start()
            return

        try:
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling()
            logger.info("Telegram bot polling started successfully!")
        except Exception as e:
            logger.error(f"Failed to start bot polling: {e}")
    
    async def stop_polling(self):
        """Stop bot polling"""
        try:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Telegram bot polling stopped")
        except Exception as e:
            logger.error(f"Failed to stop bot polling: {e}")


# Global instance
telegram_service = TelegramService()
