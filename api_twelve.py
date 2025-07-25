# pocket/api_twelve.py

import os
import requests

API_KEY = os.getenv("TWELVE_API_KEY")

def get_last_candle(symbol):
    url = f"https://api.twelvedata.com/time_series"
    params = {
        "symbol": symbol,
        "interval": "15min",
        "outputsize": 2,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data = response.json()

    if "values" in data:
        candles = data["values"]
        candle_atual = candles[0]  # mais recente
        candle_anterior = candles[1]  # anterior
        return candle_atual, candle_anterior
    else:
        print("Erro na API:", data)
        return None, None
