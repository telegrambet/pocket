import requests
import json
import os
import time
from datetime import datetime, timedelta
import pytz

CAMINHO_ARQUIVO = "sinais_cadastrados.json"
PAISES = ['EURUSD', 'EURJPY', 'EURGBP', 'GBPJPY', 'USDJPY']
TOKEN_BOT = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TIMEZONE = pytz.timezone("America/Sao_Paulo")

def get_recomendacoes(par):
    try:
        url = f"https://scanner.tradingview.com/america/scan"
        headers = {"Content-Type": "application/json"}
        payload = {
            "symbols": {"tickers": [f"OANDA:{par}"], "query": {"types": []}},
            "columns": [
                "Recommend.All", "Recommend.MA", "RSI", "RSI[1]",
                "MACD.macd", "MACD.signal", "Stoch.K", "Stoch.D",
                "Sar", "close"
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        if not data['data']:
            return None

        indicadores = data['data'][0]['d']
        return {
            "par": par,
            "recomendacao": indicadores[0],
            "sar": indicadores[8],
            "rsi": indicadores[2],
            "macd": indicadores[4],
            "macd_signal": indicadores[5],
        }
    except Exception as e:
        print(f"[ERRO TRADINGVIEW] {e}")
        return None

def verificar_sinais():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return False

    sinais_confirmados = 0
    com_sinais = False

    with open(CAMINHO_ARQUIVO, "r") as f:
        sinais = json.load(f)

    agora = datetime.now(TIMEZONE)
    for sinal in sinais:
        try:
            tempo, par, hora_str, direcao = sinal.split(";")
            hora_sinal = datetime.strptime(hora_str.strip(), "%H:%M").replace(
                year=agora.year, month=agora.month, day=agora.day, tzinfo=TIMEZONE
            )

            if hora_sinal < agora or hora_sinal > agora + timedelta(hours=1):
                continue  # fora do intervalo de 1h

            com_sinais = True

            resultado = get_recomendacoes(par)
            if not resultado:
                continue

            confirmacao = (
                resultado["recomendacao"] >= 0.5 and direcao == "CALL" or
                resultado["recomendacao"] <= -0.5 and direcao == "PUT"
            )

            rsi_confirma = (
                resultado["rsi"] > 30 and direcao == "CALL" or
                resultado["rsi"] < 70 and direcao == "PUT"
            )

            macd_confirma = (
                resultado["macd"] > resultado["macd_signal"] and direcao == "CALL" or
                resultado["macd"] < resultado["macd_signal"] and direcao == "PUT"
            )

            if confirmacao and rsi_confirma and macd_confirma:
                mensagem = f"📢 SINAL CONFIRMADO: {par} às {hora_str} ({direcao})"
                enviar_telegram(mensagem)
                sinais_confirmados += 1
        except Exception as e:
            print(f"[ERRO VERIFICAR SINAL] {e}")

    if not com_sinais:
        enviar_telegram("⚠️ Nenhum sinal cadastrado para a próxima 1 hora.")
    elif sinais_confirmados == 0:
        enviar_telegram("⏳ Nenhum sinal confirmado no momento. Aguardando próximas análises...")

def enviar_telegram(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN_BOT}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
    try:
        requests.post(url, data=payload)
    except:
        print("Erro ao enviar mensagem.")

# Loop contínuo a cada 5 minutos
if __name__ == "__main__":
    while True:
        print(f"[{datetime.now(TIMEZONE).strftime('%H:%M:%S')}] Verificando sinais...")
        verificar_sinais()
        time.sleep(300)  # espera 5 minutos
            
