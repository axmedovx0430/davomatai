from telegram import Bot, MenuButtonWebApp, WebAppInfo
from telegram.error import TelegramError
import asyncio
import logging

# Configuration
BOT_TOKEN = "8296672835:AAEKDyvLzBPAgBotc9prA9VGxZYh8d7pesk"
WEB_APP_URL = "https://b178433ada461d.lhr.life"

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
