# telegram_bot.py
import os
import telegram
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def enviar_mensagem(texto):
    try:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=texto)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")
