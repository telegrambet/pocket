from telegram.ext import ApplicationBuilder
from bot.commands import get_handlers
from bot.scheduler import start_schedulers
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

def start_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    for handler in get_handlers():
        app.add_handler(handler)

    # Iniciar agendamentos automáticos
    start_schedulers(app)

    print("✅ Bot rodando...")
    app.run_polling()

if __name__ == '__main__':
    start_bot()
