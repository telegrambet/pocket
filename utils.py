# utils.py

PAIRS = {
    'frxEURJPY': 6.1,
    'frxGBPJPY': 7.5,
    'frxCADJPY': 5.9,
    'frxAUDCAD': 4.2,
    'frxEURGBP': 3.3,
}

def calculate_pips(open_price, close_price):
    return abs(close_price - open_price) * 1000

def check_retraction_signal(symbol, candles, average_pips):
    last_candle = candles[-1]
    open_price = float(last_candle['open'])
    close_price = float(last_candle['close'])
    pips = calculate_pips(open_price, close_price)

    if pips >= average_pips:
        direction = '💥 POSSÍVEL RETRAÇÃO DE ALTA' if open_price > close_price else '💥 POSSÍVEL RETRAÇÃO DE BAIXA'
        msg = f\"\"\"\n📍 *{symbol.replace('frx', '')}*\n{direction}\nPips: {pips:.2f} (média: {average_pips})\n⏱️ Timeframe: M5\"\"\"
        return msg

    return None
