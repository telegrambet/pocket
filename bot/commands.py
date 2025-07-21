from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from bot.utils import cadastrar_sinal, listar_sinais, consultar_sinais_tecnicos
from bot.scheduler import stop_bot, restart_bot

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot iniciado!")

async def cadastrar_sinal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Uso: /cadastrarsinal PAR DIREÇÃO (ex: /cadastrarsinal EUR/USD CALL)")
        return
    par = context.args[0].upper()
    direcao = context.args[1].upper()
    resposta = cadastrar_sinal(par, direcao)
    await update.message.reply_text(resposta)

async def listar_sinais_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resposta = listar_sinais()
    await update.message.reply_text(resposta)

async def consultar_tecnico_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    resposta = consultar_sinais_tecnicos()
    await context.bot.send_message(chat_id=chat_id, text=resposta)

async def stop_bot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_bot()
    await update.message.reply_text("⛔ Bot pausado.")

async def restart_bot_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restart_bot()
    await update.message.reply_text("✅ Bot reiniciado.")

def get_handlers():
    return [
        CommandHandler("start", start),
        CommandHandler("cadastrarsinal", cadastrar_sinal_cmd),
        CommandHandler("listarsinais", listar_sinais_cmd),
        CommandHandler("consultartecnico", consultar_tecnico_cmd),
        CommandHandler("stopbot", stop_bot_cmd),
        CommandHandler("restartbot", restart_bot_cmd),
    ]
