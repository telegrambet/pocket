import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv
from InvestingScraper import scrape_investing
from TradingViewIndicators import get_indicators

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

sinais_cadastrados = []
scheduler_ref = None

def stop_analysis():
    if scheduler_ref:
        scheduler_ref.pause()

def restart_analysis():
    if scheduler_ref:
        scheduler_ref.resume()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot iniciado!")

async def stopbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    stop_analysis()
    await update.message.reply_text("⛔ Bot pausado.")

async def restartbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    restart_analysis()
    await update.message.reply_text("✅ Bot reiniciado.")

async def cadastrarsinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        texto = ' '.join(context.args)
        par, direcao = texto.split()
        sinais_cadastrados.append((par.upper(), direcao.upper()))
        await update.message.reply_text(f"Sinal cadastrado: {par.upper()} - {direcao.upper()}")
    except:
        await update.message.reply_text("❗ Formato inválido. Use: /cadastrarsinal EUR/USD CALL")

async def listarsinais(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not sinais_cadastrados:
        await update.message.reply_text("ℹ️ Nenhum sinal cadastrado.")
        return
    resposta = "\\n".join([f"{s[0]} - {s[1]}" for s in sinais_cadastrados])
    await update.message.reply_text(f"Sinais cadastrados:\\n{resposta}")

async def consultartecnico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sinais = scrape_investing()
    resposta = ""

    for par, tempos in sinais.items():
        symbol = par.replace("/", "")
        indicadores = get_indicators(symbol)
        if "erro" in indicadores:
            continue

        bloco = f"📊 {par}\\n"
        bloco += f"5M: {tempos['5M']} | 15M: {tempos['15M']} | 1H: {tempos['1H']}\\n"
        bloco += f"RSI: {indicadores['RSI']}\\nMACD: {indicadores['MACD']}\\n"
        bloco += f"Estocástico: {indicadores['Estocástico']}\\nParabolic SAR: {indicadores['SAR']}\\n"

        for s in sinais_cadastrados:
            if s[0] == par:
                if (
                    s[1] == "CALL" and
                    indicadores["RSI"] == "Sobrevendido" and
                    "para cima" in indicadores["MACD"] and
                    "para cima" in indicadores["Estocástico"] and
                    indicadores["SAR"] == "CALL"
                ) or (
                    s[1] == "PUT" and
                    indicadores["RSI"] == "Sobrecomprado" and
                    "para baixo" in indicadores["MACD"] and
                    "para baixo" in indicadores["Estocástico"] and
                    indicadores["SAR"] == "PUT"
                ):
                    bloco += "✅ Sinal Confirmado\\n"
                else:
                    bloco += "❌ Sinal NÃO confirmado\\n"
        bloco += "\\n"
        resposta += bloco

    await update.message.reply_text(resposta or "❌ Nenhum sinal técnico encontrado.")

def start_bot(scheduler):
    global scheduler_ref
    scheduler_ref = scheduler
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stopbot", stopbot))
    app.add_handler(CommandHandler("restartbot", restartbot))
    app.add_handler(CommandHandler("cadastrarsinal", cadastrarsinal))
    app.add_handler(CommandHandler("listarsinais", listarsinais))
    app.add_handler(CommandHandler("consultartecnico", consultartecnico))

    app.run_polling()
