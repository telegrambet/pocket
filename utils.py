# utils.py

PAIRS = {
    'frxEURJPY': 45.1,
    'frxGBPJPY': 45.5,
    'frxCADJPY': 45.9,
    'frxAUDJPY': 45.2,
    'frxEURGBP': 45.3,
    'frxEURUSD': 45.2,
    'frxUSDCAD': 45.2,
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
        msg = f"""
📍 *{symbol.replace('frx', '')}*
{direction}
Pips: {pips:.2f} (média: {average_pips})
⏱️ Timeframe: M5"""
        return msg

    return None
