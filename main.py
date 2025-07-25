import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from api_twelve import get_last_candle
from utils import calcular_variacao, interpretar_movimento

PARES = ["EUR/USD", "EUR/GBP", "EUR/JPY", "AUD/JPY", "GBP/JPY", "EUR/CHF"]
LIMITE_PIPS = 20

# Mensagem ao iniciar o bot manualmente com /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bem vindo, fique atento! Em breve chegarão as explosões 🚀🌟")

# Monitoramento automático a cada 15 minutos
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

        # Envia as mensagens encontradas
        if mensagens:
            for msg in mensagens:
                await app.bot.send_message(chat_id=os.getenv("TELEGRAM_CHAT_ID"), text=msg)
        else:
            print("Nenhuma explosão detectada.")

        await asyncio.sleep(15 * 60)  # Aguarda 15 minutos

# Função principal do bot
async def main():
    token = os.getenv("TELEGRAM_TOKEN")
    if not token or not os.getenv("TELEGRAM_CHAT_ID"):
        raise RuntimeError("Variáveis TELEGRAM_TOKEN ou TELEGRAM_CHAT_ID não definidas no ambiente.")

    application = ApplicationBuilder().token(token).build()

    # Handler para comando /start
    application.add_handler(CommandHandler("start", start))

    # Inicia o monitoramento em segundo plano
    asyncio.create_task(monitorar_explosoes(application))

    print("✅ Bot rodando e monitorando automaticamente...")
    await application.run_polling()

# Roda o bot automaticamente
if __name__ == "__main__":
    asyncio.run(main())
