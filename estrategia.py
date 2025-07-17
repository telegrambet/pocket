from datetime import datetime
from indicators import get_analysis, get_rsi, get_macd, get_sar

# Payout mínimo aceitável
MIN_PAYOUT = 70

# Timeframes usados para STRONG_BUY / STRONG_SELL
TIMEFRAMES_CONFIRM = ['4h', '1h', '15m', '5m']

# Confirmação total do sinal (True = válido)
def verificar_estrategia(par, direcao, payout, agora):
    if payout < MIN_PAYOUT:
        return False, 'Payout abaixo de 70%'

    # 1. STRONG_BUY/SELL nos timeframes
    for timeframe in TIMEFRAMES_CONFIRM:
        analise = get_analysis(par, timeframe)
        if direcao == 'CALL' and analise != 'STRONG_BUY':
            return False, f'Sem STRONG_BUY no {timeframe}'
        if direcao == 'PUT' and analise != 'STRONG_SELL':
            return False, f'Sem STRONG_SELL no {timeframe}'

    # 2. RSI confirmação
    rsi = get_rsi(par, '5m')
    if direcao == 'CALL' and rsi <= 30:
        return False, 'RSI ainda abaixo de 30'
    if direcao == 'CALL' and rsi > 30:
        pass  # Confirmado
    if direcao == 'PUT' and rsi >= 70:
        return False, 'RSI ainda acima de 70'
    if direcao == 'PUT' and rsi < 70:
        pass  # Confirmado

    # 3. MACD confirmação
    macd_ok = get_macd(par, '5m', direcao)
    if not macd_ok:
        return False, 'MACD não confirma'

    # 4. SAR Parabólico
    sar_ok = get_sar(par, '5m', direcao)
    if not sar_ok:
        return False, 'SAR não confirma'

    return True, 'Sinal confirmado'
  
