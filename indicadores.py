# indicadores.py
import requests

def get_summary(pair, timeframe):
    url = f"https://scanner.tradingview.com/crypto/scan"
    headers = {"Content-Type": "application/json"}
    payload = {
        "symbols": {
            "tickers": [f"OANDA:{pair}"],
            "query": {"types": []}
        },
        "columns": [
            f"Recommend.{timeframe}",
            f"RSI.{timeframe}",
            f"RSI[1].{timeframe}",
            f"MACD.macd.{timeframe}",
            f"MACD.signal.{timeframe}",
            f"SAR.{timeframe}"
        ]
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()

    try:
        d = data['data'][0]['d']
        summary = {
            'recommendation': d[0],
            'rsi': d[1],
            'rsi_prev': d[2],
            'macd': d[3],
            'macd_signal': d[4],
            'sar': d[5]
        }
        return summary
    except:
        return None

def get_all_timeframes(pair):
    timeframes = ['4h', '1h', '15', '5']
    results = {}
    for tf in timeframes:
        results[tf] = get_summary(pair, tf)
    return results
