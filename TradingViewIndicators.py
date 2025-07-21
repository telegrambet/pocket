import requests

def get_indicators(symbol):
    url = f"https://scanner.tradingview.com/america/scan"
    payload = {
        "symbols": {"tickers": [f"OANDA:{symbol}"], "query": {"types": []}},
        "columns": [
            "RSI", "MACD.macd", "MACD.signal", "Stoch.K", "Stoch.D", "SAR"
        ]
    }
    headers = {"Content-Type": "application/json"}

    try:
        res = requests.post(url, json=payload, headers=headers)
        data = res.json()
        if not data["data"]:
            return {}

        d = data["data"][0]["d"]
        rsi = d[0]
        macd = d[1]
        macd_signal = d[2]
        stoch_k = d[3]
        stoch_d = d[4]
        sar = d[5]

        return {
            "RSI": "Sobrecomprado" if rsi > 70 else "Sobrevendido" if rsi < 30 else "Neutro",
            "MACD": "Cruzando para cima" if macd > macd_signal else "Cruzando para baixo",
            "Estocástico": "Cruzando para cima" if stoch_k > stoch_d else "Cruzando para baixo",
            "SAR": "CALL" if sar < 0 else "PUT"
        }
    except Exception as e:
        return {"erro": str(e)}
