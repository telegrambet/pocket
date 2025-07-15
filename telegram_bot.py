from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, Updater
from controle import bot_ativo

import os
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

updater = Updater(TOKEN)
dispatcher = updater.dispatcher

def painel(update: Update, context: CallbackContext):
    keyboard = [[
        InlineKeyboardButton("Start bot ✅", callback_data='start'),
        InlineKeyboardButton("Stop bot ⛔", callback_data='stop')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Painel de controle:", reply_markup=reply_markup)

def botao(update: Update, context: CallbackContext):
    global bot_ativo
    query = update.callback_query
    query.answer()
    if query.data == 'start':
        bot_ativo = True
        query.edit_message_text("Bot reativado ✅")
    elif query.data == 'stop':
        bot_ativo = False
        query.edit_message_text("Bot pausado ⛔")

dispatcher.add_handler(CommandHandler("painel", painel))
dispatcher.add_handler(CallbackQueryHandler(botao))
