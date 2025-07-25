import os
import asyncio
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
            print("Nenhuma explosão detectada.")

        await asyncio.sleep(15 * 60)  # 15 minutos

async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    application = ApplicationBuilder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    # Inicia a tarefa de monitoramento assíncrono
    asyncio.create_task(monitorar_explosoes(application))

    print("Bot rodando com monitoramento automático...")
    await application.run_polling()

if __name__ == "__main__":
    # NÃO usar asyncio.run aqui para evitar conflito no loop de eventos
    import asyncio
    asyncio.get_event_loop().run_until_complete(main())
