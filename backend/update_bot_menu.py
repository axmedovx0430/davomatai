from telegram import Bot, MenuButtonWebApp, WebAppInfo
from telegram.error import TelegramError
import asyncio
import logging
from config import settings

# Configuration
BOT_TOKEN = settings.TELEGRAM_BOT_TOKEN
WEB_APP_URL = f"{settings.frontend_url}/mobile"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def update_menu_button():
    bot = Bot(token=BOT_TOKEN)
    try:
        await bot.set_chat_menu_button(
            menu_button=MenuButtonWebApp(
                text="Ilovani ochish",
                web_app=WebAppInfo(url=WEB_APP_URL)
            )
        )
        logger.info(f"Successfully updated menu button to: {WEB_APP_URL}")
    except TelegramError as e:
        logger.error(f"Failed to update menu button: {e}")

if __name__ == "__main__":
    asyncio.run(update_menu_button())
