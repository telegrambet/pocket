from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
from sinais import adicionar_sinal, excluir_sinais, listar_sinais
from scheduler import iniciar_agendamento
from config import TOKEN

async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Cadastrar sinais", callback_data='cadastrar')],
        [InlineKeyboardButton("Excluir sinais", callback_data='excluir')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bot de Sinais Pocket Option 💹", reply_markup=reply_markup)

async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'cadastrar':
        await query.edit_message_text("Envie os sinais no formato:\n`M5;EURUSD;07:10;CALL`", parse_mode='Markdown')
        context.user_data['cadastrando'] = True

    elif query.data == 'excluir':
        excluir_sinais()
        await query.edit_message_text("Todos os sinais cadastrados foram excluídos com sucesso!")

async def mensagem_handler(update: Update, context: CallbackContext):
    if context.user_data.get('cadastrando'):
        texto = update.message.text.strip().upper()
        if adicionar_sinal(texto):
            await update.message.reply_text("✅ Sinal cadastrado com sucesso!")
        else:
            await update.message.reply_text("❌ Formato inválido! Use: M5;EURUSD;07:10;CALL")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sinais", lambda u, c: u.message.reply_text(str(listar_sinais()))))
    app.add_handler(CommandHandler("excluir_sinais", lambda u, c: (excluir_sinais(), u.message.reply_text("Sinais excluídos!"))))
    app.add_handler(telegram.ext.CallbackQueryHandler(button_handler))
    app.add_handler(telegram.ext.MessageHandler(telegram.ext.filters.TEXT, mensagem_handler))

    iniciar_agendamento(app)
    app.run_polling()

if __name__ == "__main__":
    main()
