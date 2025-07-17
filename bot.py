import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Puxa variáveis do ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Configuração dos logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Start bot", callback_data='start_bot')],
        [InlineKeyboardButton("Stop bot", callback_data='stop_bot')],
        [InlineKeyboardButton("Cadastrar sinais", callback_data='cadastrar_sinais')],
        [InlineKeyboardButton("Excluir sinais", callback_data='excluir_sinais')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bom dia Trader, estamos em operação 💸🤖\nSaldo da banca: $0.00",
        reply_markup=reply_markup
    )

# Botões Inline
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start_bot':
        await query.edit_message_text("✅ Bot reativado!")
    elif query.data == 'stop_bot':
        await query.edit_message_text("⛔ Bot pausado.")
    elif query.data == 'cadastrar_sinais':
        await query.edit_message_text("✍️ Envie os sinais no formato:\n`M5;EURUSD;14:30;CALL`", parse_mode='Markdown')
    elif query.data == 'excluir_sinais':
        await query.edit_message_text("🗑️ Todos os sinais cadastrados foram excluídos.")

# Função principal
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

    application.run_polling()

if __name__ == "__main__":
    main()
    
