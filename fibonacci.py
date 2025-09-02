# fibonacci.py
import numpy as np
from deriv import get_candles  # já puxa os candles que você usa
from utils import PAIRS

# Níveis de Fibonacci comuns
FIB_LEVELS = [0.236, 0.382, 0.5, 0.618, 0.786]

def calculate_fibonacci(high, low):
    """
    Calcula os níveis de Fibonacci dado um high e low
    """
    diff = high - low
    return {str(level): high - (diff * level) for level in FIB_LEVELS}

def check_fibonacci_touch(pair, candles=100):
    """
    Verifica se o preço atual tocou algum nível de Fibonacci
    """
    # Puxa os candles
    data = get_candles(pair, candles)

    if not data or "candles" not in data:
        return None

    closes = [c["close"] for c in data["candles"]]
    high = max(closes)
    low = min(closes)
    last_price = closes[-1]

    fibs = calculate_fibonacci(high, low)

    for level, price in fibs.items():
        if abs(last_price - price) <= 0.0005:  # margem de tolerância
            return f"{pair} tocou no nível {level} da Fibonacci ({round(price, 5)})"

    return None
    
