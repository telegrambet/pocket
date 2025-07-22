import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder
from bot.handlers import setup_handlers
from bot.scheduler import start_scheduler

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
app = ApplicationBuilder().token(TOKEN).build()

setup_handlers(app)
start_scheduler(app)

if __name__ == "__main__":
    app.run_polling()
