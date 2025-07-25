import os
import time
import asyncio
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

from api_twelve import get_last_candle
from utils import calcular_variacao, interpretar_movimento

PARES = ["EUR/USD", "EUR/GBP", "EUR/JPY", "AUD/JPY", "GBP/JPY", "EUR/CHF"]
LIMITE_PIPS = 20

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bem vindo, fique atento! Em breve chegarão as explosões 🚀🌟"
    )

async def monitorar_explosoes(app):
    while True:
        mensagens = []
        for par in PARES:
            symbol = par.replace("/", "")
            candle_atual, _ = get_last_candle(symbol)
            if candle_atual:
                open_price = candle_atual["open"]
                close_price = candle_atual["close"]
                variacao = calcular_variacao(open_price, close_price)
                direcao, texto_pips = interpretar_movimento(variacao)
                if direcao:
                    msg = (
                        f"🚨 Explosão Direcional Detectada\n"
                        f"📍 Par: {par}\n"
                        f"🕒 Timeframe: M15\n"
                        f"📈 Direção dominante: {direcao}\n"
                        f"📊 Velocidade: {texto_pips} em 10 minutos\n"
                        f"🎯 Possível retração ou continuação forte!"
                    )
                    mensagens.append(msg)

        if mensagens:
            for mensagem in mensagens:
                await app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=mensagem)
        else:
            print(f"{datetime.utcnow()} - Nenhuma explosão detectada.")

        await asyncio.sleep(15 * 60)  # espera 15 minutos

async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    # Start a task to monitor explosions in background
    application.job_queue.run_once(lambda ctx: asyncio.create_task(monitorar_explosoes(application)), when=0)

    print("Bot rodando com monitoramento automático...")
    await application.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
