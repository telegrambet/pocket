# tradingview.py

import requests

def get_signal(pair, interval):
    url = f"https://scanner.tradingview.com/crypto/scan"
    headers = {'Content-Type': 'application/json'}
    
    payload = {
        "symbols": {
            "tickers": [f"OANDA:{pair}"],
            "query": {"types": []}
        },
        "columns": [
            f"Recommend.Other",
            f"Recommend.All",
            f"Recommend.MA",
            "RSI",
            "MACD.macd",
            "MACD.signal",
            "SAR"
        ]
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()

        if not data["data"]:
            return None

        result = data["data"][0]["d"]
        return {
            "recommendation": result[1],  # Recommend.All
            "rsi": result[3],
            "macd": result[4],
            "macd_signal": result[5],
            "sar": result[6]
        }
    except Exception as e:
        print(f"Erro ao buscar sinais para {pair}: {e}")
        return None
      
