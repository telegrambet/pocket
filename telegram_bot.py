from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, ApplicationBuilder, CallbackQueryHandler
import os
from controle import bot_ativo
from pocket_option import obter_saldo

TOKEN = os.getenv("TELEGRAM_TOKEN")

async def start(update: Update, context: CallbackContext):
    saldo = obter_saldo()
    keyboard = [
        [InlineKeyboardButton("🔴 Stop bot", callback_data="stop")],
        [InlineKeyboardButton("🟢 Reiniciar bot", callback_data="start")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"Bom dia Trader, estamos em operação 💸🤖\n\n💰 Saldo atual: ${saldo}",
        reply_markup=reply_markup
    )

async def botao_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == "start":
        context.bot_data["bot_ativo"] = True
        await query.edit_message_text("🟢 Bot reativado com sucesso!")
    elif query.data == "stop":
        context.bot_data["bot_ativo"] = False
        await query.edit_message_text("🔴 Bot pausado!")

def iniciar_telegram_bot():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(botao_handler))
    application.bot_data["bot_ativo"] = True
    application.run_polling()
