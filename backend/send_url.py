
import asyncio
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from config import settings
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def send_new_url():
    """Send the new URL directly to the admin user"""
    try:
        bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
        
        # Construct the Web App URL
        web_app_url = f"{settings.FRONTEND_URL}/mobile.html"
        logger.info(f"Sending URL: {web_app_url}")
        
        # Create a button with the new URL
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(text="📱 YANGI ILOVANI OCHISH (CLICK ME)", web_app=WebAppInfo(url=web_app_url))]
        ])
        
        # Send to all admins
        for chat_id in settings.admin_chat_ids:
            try:
                await bot.send_message(
                    chat_id=chat_id,
                    text="⚠️ **DIQQAT!**\n\nEski tugma ishlamayapti (keshlanib qolgan).\n\nIltimos, pastdagi **YANGI** tugmani bosing:",
                    reply_markup=keyboard,
                    parse_mode="Markdown"
                )
                logger.info(f"Sent to {chat_id}")
            except Exception as e:
                logger.error(f"Failed to send to {chat_id}: {e}")
        
    except Exception as e:
        logger.error(f"Failed to send URL: {e}")

if __name__ == "__main__":
    asyncio.run(send_new_url())
