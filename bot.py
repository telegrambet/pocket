import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Pega o token e chat_id do ambiente
TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Verificação básica no log
print("✅ Iniciando bot...")
if not TOKEN:
    print("❌ Erro: TELEGRAM_TOKEN não encontrado nas variáveis de ambiente!")
else:
    print("✅ Token encontrado, iniciando polling...")

# Função do comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Fala jogador! ⚽🥇 Bot funcionando com sucesso!")

# Inicializa e roda o bot
if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
