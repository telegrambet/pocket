from telegram.ext import CommandHandler, CallbackQueryHandler
from bot.commands import (
    start,
    cadastrar_sinais,
    consultar_sinais,
    consultar_tecnicos,
    stop_bot,
    restart_bot,
    botao_callback
)

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cadastrar", cadastrar_sinais))
    app.add_handler(CommandHandler("consultar", consultar_sinais))
    app.add_handler(CommandHandler("tecnicos", consultar_tecnicos))
    app.add_handler(CommandHandler("stop", stop_bot))
    app.add_handler(CommandHandler("restart", restart_bot))
    app.add_handler(CallbackQueryHandler(botao_callback))
