# telegram_bot.py
import os
import telegram
from telegram.constants import ParseMode
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

async def send_alert(message):
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, parse_mode=ParseMode.MARKDOWN)

async def send_welcome():
    msg = "👋 Olá, trader!\n\nBot de retração iniciado com sucesso.\nAguardando sinais... 🔎📉📈"
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
