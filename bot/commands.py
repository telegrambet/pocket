from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils import (
    salvar_sinais,
    ler_sinais,
    verificar_sinais_tecnicos,
    status_indicadores
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cadastrar Sinais", callback_data='cadastrar')],
        [InlineKeyboardButton("Consultar Sinais", callback_data='consultar')],
        [InlineKeyboardButton("Consultar Técnicos", callback_data='tecnicos')],
        [InlineKeyboardButton("STOP", callback_data='stop')],
        [InlineKeyboardButton("RESTART", callback_data='restart')],
    ]
    await update.message.reply_text(
        "Bot de Sinais Técnicos", reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def cadastrar_sinais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    salvar_sinais(texto)
    await update.message.reply_text("✅ Sinais cadastrados com sucesso!")

async def consultar_sinais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinais = ler_sinais()
    await update.message.reply_text(f"📌 Sinais cadastrados:\n{sinais}")

async def consultar_tecnicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = verificar_sinais_tecnicos()
    await update.message.reply_text(f"📊 Resultado técnico:\n{resultado}")

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛔ Bot pausado.")

async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot reiniciado.")

async def botao_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data
    comandos = {
        'cadastrar': cadastrar_sinais,
        'consultar': consultar_sinais,
        'tecnicos': consultar_tecnicos,
        'stop': stop_bot,
        'restart': restart_bot
    }
    if data in comandos:
        await comandos[data](update, context)
