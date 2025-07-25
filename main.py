import requests
import time
from datetime import datetime
import telegram

# CONFIGURAÇÕES
API_KEY = '8e3fac5da9594051a2bd3e5b380d4ed6'
TELEGRAM_TOKEN = 'SEU_TOKEN_DO_BOT'
TELEGRAM_CHAT_ID = 'SEU_CHAT_ID'
SYMBOLS = ["EUR/USD", "EUR/GBP", "EUR/JPY", "AUD/JPY", "GBP/JPY", "EUR/CHF"]
THRESHOLD_PIPS = 25  # Ex: 25 pips de movimento

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def get_candle(symbol):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval=15min&outputsize=1&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data['values'][0]  # Último candle

def get_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return float(data['price'])

def monitor_explosion(symbol):
    candle = get_candle(symbol)
    open_price = float(candle['open'])
    start_time = datetime.strptime(candle['datetime'], '%Y-%m-%d %H:%M:%S')

    print(f"[{symbol}] Abertura M15: {open_price} às {start_time.strftime('%H:%M')}")

    # Aguarda 10 minutos
    time.sleep(600)

    # Preço atual após 10 minutos
    current_price = get_price(symbol)
    diff = (current_price - open_price) * 10000  # em pips

    direction = "Alta" if diff > 0 else "Baixa"
    diff_abs = abs(diff)

    if diff_abs >= THRESHOLD_PIPS:
        message = (
            f"🚨 Explosão Direcional Detectada\n\n"
            f"📍 Par: {symbol.replace('/', '')}\n"
            f"🕒 Timeframe: M15\n"
            f"⏱️ Tempo de análise: primeiros 10 minutos do candle\n"
            f"📈 Direção dominante: {direction}\n"
            f"📊 Velocidade: {'+' if diff > 0 else '-'}{int(diff_abs)} pips em 10 minutos\n"
            f"📬 Tempo restante no candle: 5 minutos\n"
            f"🎯 Possível retração ou continuação forte!"
        )
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)
        print(f"[{symbol}] Alerta enviado.")

# LOOP CONTÍNUO
while True:
    now = datetime.now()
    if now.minute % 15 == 0 and now.second < 5:  # A cada novo candle M15
        for symbol in SYMBOLS:
            try:
                monitor_explosion(symbol)
            except Exception as e:
                print(f"Erro em {symbol}: {e}")
        time.sleep(900)  # Aguarda 15 minutos para o próximo candle
    time.sleep(1)
  
