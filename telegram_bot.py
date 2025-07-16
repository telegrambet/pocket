from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler
import os
from pocket_option import obter_saldo  # função que retorna saldo da conta real

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id

    # Mensagem principal
    mensagem = "Bom dia Trader, estamos em operação 💸🤖\n\n"
    saldo = obter_saldo()
    mensagem += f"💰 Seu saldo atual: ${saldo}"

    # Botões visuais
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
        query.edit_message_text("⛔ Bot pausado (visual). Ele continua automático das 6h às 11h.")
    elif query.data == "restart_bot":
        query.edit_message_text("🔁 Bot reiniciado (visual). Ele roda automaticamente às 6h.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(tratar_botoes))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
    
