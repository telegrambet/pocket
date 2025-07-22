import logging
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot.handlers import setup_handlers

load_dotenv()

import os

TOKEN = os.getenv("TELEGRAM_TOKEN")

logging.basicConfig(level=logging.INFO)
app = ApplicationBuilder().token(TOKEN).build()
setup_handlers(app)

if __name__ == "__main__":
    app.run_polling()
