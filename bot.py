import logging
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# Variáveis com token e chat_id
TOKEN_BOT = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Caminho do arquivo de sinais
CAMINHO_ARQUIVO = "sinais_cadastrados.json"

# Configura os logs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Função de saudação
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Start bot", callback_data='start_bot')],
        [InlineKeyboardButton("Stop bot", callback_data='stop_bot')],
        [InlineKeyboardButton("Cadastrar sinais", callback_data='cadastrar_sinais')],
        [InlineKeyboardButton("Excluir sinais", callback_data='excluir_sinais')],
        [InlineKeyboardButton("Visualizar sinais", callback_data='visualizar_sinais')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bom dia Trader, estamos em operação 💸🤖\nSaldo da banca: $0.00",
        reply_markup=reply_markup
    )

# Botões
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start_bot':
        await query.edit_message_text("✅ Bot reativado!")
    elif query.data == 'stop_bot':
        await query.edit_message_text("⛔ Bot pausado.")
    elif query.data == 'cadastrar_sinais':
        await query.edit_message_text("✍️ Envie os sinais no formato:\n`M5;EURUSD;14:30;CALL`", parse_mode='Markdown')
        context.user_data["esperando_sinal"] = True
    elif query.data == 'excluir_sinais':
        if os.path.exists(CAMINHO_ARQUIVO):
            os.remove(CAMINHO_ARQUIVO)
        await query.edit_message_text("🗑️ Todos os sinais cadastrados foram excluídos.")
    elif query.data == 'visualizar_sinais':
        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, "r") as f:
                sinais = json.load(f)
            if sinais:
                resposta = "\n".join(sinais)
            else:
                resposta = "⚠️ Nenhum sinal cadastrado."
        else:
            resposta = "⚠️ Nenhum sinal cadastrado."
        await query.edit_message_text(resposta)

# Receber sinal digitado
async def receber_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("esperando_sinal"):
        texto = update.message.text.strip()
        linhas = texto.split("\n")
        sinais_validos = []

        for linha in linhas:
            linha = linha.strip()
            if validar_sinal(linha):
                sinais_validos.append(linha)

        if sinais_validos:
            sinais = []
            if os.path.exists(CAMINHO_ARQUIVO):
                with open(CAMINHO_ARQUIVO, "r") as f:
                    sinais = json.load(f)

            sinais.extend(sinais_validos)

            with open(CAMINHO_ARQUIVO, "w") as f:
                json.dump(sinais, f, indent=4)

            await update.message.reply_text(f"✅ {len(sinais_validos)} sinal(is) cadastrado(s) com sucesso!")
        else:
            await update.message.reply_text("❌ Nenhum sinal válido encontrado. Use:\n`M5;EURUSD;14:30;CALL`", parse_mode='Markdown')

        context.user_data["esperando_sinal"] = False

# Validação do sinal
def validar_sinal(texto):
    partes = texto.split(";")
    return len(partes) == 4 and partes[0] in ["M1", "M5", "M15"] and partes[3].upper() in ["CALL", "PUT"]

# Função principal
def main():
    application = Application.builder().token(TOKEN_BOT).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_sinal))

    application.run_polling()

if __name__ == "__main__":
    main()
