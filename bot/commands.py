from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from bot.utils import salvar_sinais, ler_sinais, verificar_sinais_tecnicos

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cadastrar Sinais", callback_data='cadastrar')],
        [InlineKeyboardButton("Consultar Sinais", callback_data='consultar')],
        [InlineKeyboardButton("Consultar Técnicos", callback_data='tecnicos')],
        [InlineKeyboardButton("STOP", callback_data='stop')],
        [InlineKeyboardButton("RESTART", callback_data='restart')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bot de Sinais Técnicos - Escolha uma opção:", reply_markup=reply_markup)

async def cadastrar_sinais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = " ".join(context.args)
    if not texto:
        await update.message.reply_text("Envie os sinais no formato:\nM5;AUDCAD;06:10;CALL")
        return
    salvar_sinais(texto)
    await update.message.reply_text("✅ Sinais cadastrados com sucesso!")

async def consultar_sinais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinais = ler_sinais()
    await update.message.reply_text(f"📌 Sinais cadastrados:\n{sinais}")

async def consultar_tecnicos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    resultado = verificar_sinais_tecnicos()
    await update.message.reply_text(f"📊 Resultado técnico:\n{resultado}")

async def stop_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Implementar flag para parar scheduler
    context.application.bot_data["running"] = False
    await update.message.reply_text("⛔ Bot pausado.")

async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Implementar flag para iniciar scheduler
    context.application.bot_data["running"] = True
    await update.message.reply_text("✅ Bot reiniciado.")

async def botao_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "cadastrar":
        await query.edit_message_text("Envie os sinais no formato:\nM5;AUDCAD;06:10;CALL")
    elif data == "consultar":
        sinais = ler_sinais()
        await query.edit_message_text(f"📌 Sinais cadastrados:\n{sinais}")
    elif data == "tecnicos":
        resultado = verificar_sinais_tecnicos()
        await query.edit_message_text(f"📊 Resultado técnico:\n{resultado}")
    elif data == "stop":
        context.application.bot_data["running"] = False
        await query.edit_message_text("⛔ Bot pausado.")
    elif data == "restart":
        context.application.bot_data["running"] = True
        await query.edit_message_text("✅ Bot reiniciado.")
    else:
        await query.edit_message_text("Opção inválida.")
