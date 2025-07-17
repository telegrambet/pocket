# indicadores.py

def rsi_confirmado(rsi, direcao):
    if direcao == "CALL" and rsi > 30:
        return True
    if direcao == "PUT" and rsi < 70:
        return True
    return False

def macd_confirmado(macd, macd_signal, direcao):
    if direcao == "CALL" and macd > macd_signal:
        return True
    if direcao == "PUT" and macd < macd_signal:
        return True
    return False

def sar_confirmado(sar_value, direcao):
    if direcao == "CALL" and sar_value == 1:
        return True
    if direcao == "PUT" and sar_value == -1:
        return True
    return False
