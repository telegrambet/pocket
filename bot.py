import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os

# Caminho para armazenar os sinais
CAMINHO_ARQUIVO_SINAIS = "sinais_cadastrados.json"

# Função para salvar os sinais
def salvar_sinais(sinais):
    with open(CAMINHO_ARQUIVO_SINAIS, "w") as f:
        json.dump(sinais, f, indent=4)

# Função para carregar os sinais
def carregar_sinais():
    if not os.path.exists(CAMINHO_ARQUIVO_SINAIS):
        return []
    with open(CAMINHO_ARQUIVO_SINAIS, "r") as f:
        return json.load(f)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cadastrar sinais", callback_data="cadastrar_sinais")],
        [InlineKeyboardButton("Excluir sinais", callback_data="excluir_sinais")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Olá! Escolha uma opção:", reply_markup=reply_markup)

# Botões
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cadastrar_sinais":
        await query.edit_message_text("Envie os sinais no formato:\n\nM5;EURUSD;14:30;CALL")
        context.user_data["cadastrando_sinais"] = True

    elif query.data == "excluir_sinais":
        salvar_sinais([])  # limpa todos os sinais
        await query.edit_message_text("✅ Todos os sinais foram excluídos com sucesso.")

# Lógica para cadastrar sinais
async def tratar_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("cadastrando_sinais"):
        sinais_recebidos = update.message.text.split("\n")
        sinais_validos = []
        for linha in sinais_recebidos:
            partes = linha.strip().split(";")
            if len(partes) == 4:
                timeframe, par, horario, direcao = partes
                if timeframe == "M5" and direcao.upper() in ["CALL", "PUT"]:
                    sinais_validos.append(linha.strip())
                else:
                    await update.message.reply_text("❌ Formato inválido. Use:\nM5;EURUSD;14:30;CALL")
                    return
            else:
                await update.message.reply_text("❌ Formato inválido. Use:\nM5;EURUSD;14:30;CALL")
                return

        sinais_existentes = carregar_sinais()
        sinais_existentes.extend(sinais_validos)
        salvar_sinais(sinais_existentes)

        context.user_data["cadastrando_sinais"] = False

        resposta = "\n".join(sinais_validos)
        await update.message.reply_text(f"✅ Sinais cadastrados:\n\n{resposta}")

# Inicialização
if __name__ == "__main__":
    import asyncio

    async def main():
        token = os.getenv("TELEGRAM_TOKEN")
        app = ApplicationBuilder().token(token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), tratar_mensagem))

        print("Bot rodando...")
        await app.run_polling()

    asyncio.run(main())
                    
