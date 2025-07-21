from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from bot.commands import (
    start,
    cadastrar_sinal,
    listar_sinais,
    consultar_sinais_tecnicos,
    stop_bot,
    restart_bot
)

def main():
    app = ApplicationBuilder().token("SEU_TOKEN_AQUI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cadastrarsinal", cadastrar_sinal))
    app.add_handler(CommandHandler("listarsinais", listar_sinais))
    app.add_handler(CommandHandler("consultartecnico", consultar_sinais_tecnicos))
    app.add_handler(CommandHandler("stopbot", stop_bot))
    app.add_handler(CommandHandler("restartbot", restart_bot))

    app.run_polling()
