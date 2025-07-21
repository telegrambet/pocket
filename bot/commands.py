from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from bot.utils import (
    cadastrar_sinal, listar_sinais, consultar_sinais_tecnicos,
    start_bot, stop_bot, restart_bot
)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("🤖 Bot iniciado!")

def cadastrar_sinal_cmd(update: Update, context: CallbackContext):
    if len(context.args) < 2:
        update.message.reply_text("Uso: /cadastrarsinal PAR DIREÇÃO (ex: /cadastrarsinal EUR/USD CALL)")
        return
    par = context.args[0].upper()
    direcao = context.args[1].upper()
    resposta = cadastrar_sinal(par, direcao)
    update.message.reply_text(resposta)

def listar_sinais_cmd(update: Update, context: CallbackContext):
    resposta = listar_sinais()
    update.message.reply_text(resposta)

def consultar_tecnico_cmd(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    resposta = consultar_sinais_tecnicos()
    context.bot.send_message(chat_id=chat_id, text=resposta)

def stop_bot_cmd(update: Update, context: CallbackContext):
    stop_bot()
    update.message.reply_text("⛔ Bot pausado.")

def restart_bot_cmd(update: Update, context: CallbackContext):
    restart_bot()
    update.message.reply_text("✅ Bot reiniciado.")

def get_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("cadastrarsinal", cadastrar_sinal_cmd),
        CommandHandler("listarsinais", listar_sinais_cmd),
        CommandHandler("consultartecnico", consultar_tecnico_cmd),
        CommandHandler("stopbot", stop_bot_cmd),
        CommandHandler("restartbot", restart_bot_cmd),
    ]
