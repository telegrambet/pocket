import logging
import json
import os
import asyncio
import datetime
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters
)

TOKEN_BOT = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CAMINHO_ARQUIVO = "sinais_cadastrados.json"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === Funções de análise técnica ===

def verificar_sinal_tecnico(par):
    try:
        url = f"https://scanner.tradingview.com/america/scan"
        headers = {'Content-Type': 'application/json'}
        timeframes = ["5", "15", "60", "240"]
        confirmacoes = {}

        for tf in timeframes:
            payload = {
                "symbols": {"tickers": [f"OANDA:{par}"], "query": {"types": []}},
                "columns": [f"Recommend.{tf}"]
            }
            r = requests.post(url, json=payload, headers=headers)
            data = r.json()
            recomend = data['data'][0]['d'][0]
            confirmacoes[tf] = recomend

        # Verifica se todos são STRONG_BUY ou STRONG_SELL
        if all(r == "STRONG_BUY" for r in confirmacoes.values()):
            direcao = "CALL"
        elif all(r == "STRONG_SELL" for r in confirmacoes.values()):
            direcao = "PUT"
        else:
            return None

        # Indicadores no M5
        payload = {
            "symbols": {"tickers": [f"OANDA:{par}"], "query": {"types": []}},
            "columns": ["RSI", "MACD.macd", "MACD.signal", "SAR"]
        }
        r = requests.post(url, json=payload, headers=headers)
        d = r.json()["data"][0]["d"]
        rsi, macd, macd_signal, sar = d

        if not ((direcao == "CALL" and rsi > 30 and macd > macd_signal and sar == 1) or
                (direcao == "PUT" and rsi < 70 and macd < macd_signal and sar == -1)):
            return None

        return direcao

    except Exception as e:
        print(f"Erro TradingView: {e}")
        return None

# === Botões ===

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

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'start_bot':
        context.bot_data["verificando"] = True
        await query.edit_message_text("✅ Bot reativado!")
    elif query.data == 'stop_bot':
        context.bot_data["verificando"] = False
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

# === Receber e validar sinal ===

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

def validar_sinal(texto):
    partes = texto.split(";")
    return len(partes) == 4 and partes[0] in ["M1", "M5", "M15"] and partes[3].upper() in ["CALL", "PUT"]

# === Verificação automática ===

async def loop_verificacao(application: Application):
    while True:
        await asyncio.sleep(60)

        if not application.bot_data.get("verificando"):
            continue

        if os.path.exists(CAMINHO_ARQUIVO):
            with open(CAMINHO_ARQUIVO, "r") as f:
                sinais = json.load(f)
        else:
            sinais = []

        agora = datetime.datetime.now().strftime("%H:%M")
        pares = list(set([s.split(";")[1] for s in sinais])) or ["EURUSD", "USDJPY", "GBPUSD", "EURGBP"]

        for par in pares:
            direcao = verificar_sinal_tecnico(par)
            if not direcao:
                continue

            encontrado = False
            for sinal in sinais:
                tf, p, hora, dir_ = sinal.split(";")
                if p.upper() == par.upper() and dir_.upper() == direcao and hora == agora:
                    encontrado = True
                    break

            msg = (f"🚨 Sinal compatível com cadastrado: {par} às {agora} - {direcao}"
                   if encontrado else
                   f"⚠️ Sinal técnico confirmado: {par} às {agora} - {direcao} (sem cadastro manual)")
            await application.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

# === Main ===

def main():
    application = Application.builder().token(TOKEN_BOT).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_sinal))

    application.bot_data["verificando"] = True
    application.create_task(loop_verificacao(application))

    application.run_polling()

if __name__ == "__main__":
    main()
