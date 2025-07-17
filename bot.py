import asyncio
import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from signals import (
    carregar_sinais,
    cadastrar_sinal,
    excluir_todos_sinais,
    buscar_sinais_cadastrados,
)
from tradingview_scraper import buscar_sinal_tecnico
from datetime import datetime, timedelta

# Carregar variáveis de ambiente
load_dotenv()
TOKEN_BOT = os.getenv("TOKEN_BOT")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Ativar logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pares_suportados = ["EURUSD", "EURJPY", "EURGBP", "GBPJPY", "USDJPY"]

# START
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cadastrar sinais", callback_data="cadastrar")],
        [InlineKeyboardButton("Excluir sinais", callback_data="excluir")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo, meu trader 🤖💸", reply_markup=reply_markup)

# CALLBACK DOS BOTÕES
async def botoes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cadastrar":
        await query.edit_message_text("Envie o sinal no formato: `M5;PAR;HORA;DIREÇÃO`", parse_mode='Markdown')
    elif query.data == "excluir":
        excluir_todos_sinais()
        await query.edit_message_text("Todos os sinais foram excluídos.")

# RECEBER NOVO SINAL
async def receber_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = update.message.text.strip().upper()
    if ";" in texto:
        try:
            tempo, par, hora, direcao = texto.split(";")
            sinal = {
                "tempo": tempo,
                "par": par,
                "hora": hora,
                "direcao": direcao
            }
            cadastrar_sinal(sinal)
            await update.message.reply_text(f"Sinal cadastrado com sucesso: {sinal}")
        except:
            await update.message.reply_text("Formato inválido. Use: M5;PAR;HORA;DIREÇÃO")
    else:
        await update.message.reply_text("Formato inválido. Use: M5;PAR;HORA;DIREÇÃO")

# VERIFICADOR DE SINAIS TÉCNICOS + COMPARAÇÃO
async def verificar_sinais():
    while True:
        sinais_tecnicos = buscar_sinal_tecnico()
        sinais_cadastrados = buscar_sinais_cadastrados()
        agora = datetime.now()

        for par in pares_suportados:
            info = sinais_tecnicos.get(par)
            if not info:
                continue

            direcao = info.get("sinal")  # STRONG_BUY ou STRONG_SELL
            if direcao not in ["STRONG_BUY", "STRONG_SELL"]:
                continue

            rsi = info.get("RSI")
            macd = info.get("MACD")
            estocastico = info.get("STOCH")

            if not (rsi and macd and estocastico):
                continue

            for sinal_manual in sinais_cadastrados:
                if sinal_manual["par"] != par:
                    continue

                if direcao.endswith("BUY") and sinal_manual["direcao"] != "CALL":
                    continue
                if direcao.endswith("SELL") and sinal_manual["direcao"] != "PUT":
                    continue

                # Verificar se está dentro da 1h de tolerância
                hora_sinal = datetime.strptime(sinal_manual["hora"], "%H:%M")
                hora_sinal = agora.replace(hour=hora_sinal.hour, minute=hora_sinal.minute, second=0, microsecond=0)
                if agora <= hora_sinal <= agora + timedelta(hours=1):
                    mensagem = (
                        f"📊 SINAL CONFIRMADO!\n\n"
                        f"⏱️ Tempo: {sinal_manual['tempo']}\n"
                        f"💱 Par: {par}\n"
                        f"📌 Direção: {sinal_manual['direcao']}\n"
                        f"📉 Técnicos: {direcao}, RSI: {rsi}, MACD: {macd}, STOCH: {estocastico}"
                    )
                    await enviar_mensagem(mensagem)
        await asyncio.sleep(60)  # Verifica a cada minuto

# ENVIO DE MENSAGEM
async def enviar_mensagem(texto):
    from telegram import Bot
    bot = Bot(token=TOKEN_BOT)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=texto)

# MAIN
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN_BOT).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botoes))
    app.add_handler(CommandHandler("verificar", lambda u, c: verificar_sinais()))
    app.add_handler(CommandHandler("enviar", lambda u, c: enviar_mensagem("Teste")))

    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_sinal))

    # Rodar o verificador em segundo plano
    app.create_task(verificar_sinais())

    app.run_polling()
