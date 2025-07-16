from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import os
from pocket_option import obter_saldo
import controle

TOKEN = os.getenv("TELEGRAM_TOKEN")

# Variáveis globais para envio externo
bot_instance = None
chat_id_geral = None

def start(update: Update, context: CallbackContext):
    global chat_id_geral
    chat_id = update.effective_chat.id
    chat_id_geral = chat_id

    saldo = obter_saldo()
    mensagem = "Bom dia Trader, estamos em operação 💸🤖\n\n"
    mensagem += f"💰 Seu saldo atual: ${saldo}"

    botoes = [
        [InlineKeyboardButton("⛔ Stop bot", callback_data="stop_bot")],
        [InlineKeyboardButton("🔁 Reiniciar bot", callback_data="restart_bot")]
    ]
    reply_markup = InlineKeyboardMarkup(botoes)

    context.bot.send_message(chat_id=chat_id, text=mensagem, reply_markup=reply_markup)

def tratar_botoes(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "stop_bot":
        controle.bot_ativo = False
        query.edit_message_text("⛔ Bot pausado manualmente. Ele não fará operações.")
    elif query.data == "restart_bot":
        controle.bot_ativo = True
        query.edit_message_text("🔁 Bot reativado manualmente. Ele voltará a operar das 6h às 11h.")

def enviar_mensagem(texto):
    if bot_instance and chat_id_geral:
        bot_instance.send_message(chat_id=chat_id_geral, text=texto)

def main():
    global bot_instance
    updater = Updater(TOKEN, use_context=True)
    bot_instance = updater.bot

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(tratar_botoes))

    updater.start_polling()
    updater.idle()
    
