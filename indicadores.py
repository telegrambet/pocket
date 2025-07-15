import pandas as pd
from ta.trend import PSARIndicator
from ta.momentum import RSIIndicator
from ta.trend import MACD

def calcular_indicadores(df):
    df['psar'] = PSARIndicator(df['high'], df['low'], df['close']).psar()
    df['rsi'] = RSIIndicator(df['close']).rsi()
    macd = MACD(df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def validar_sar(df, direcao):
    ultimo = df.iloc[-1]
    if direcao == "STRONG_BUY" and ultimo['close'] > ultimo['psar']:
        return True
    if direcao == "STRONG_SELL" and ultimo['close'] < ultimo['psar']:
        return True
    return False

def cruzou_rsi(df, direcao):
    rsi = df['rsi']
    if direcao == "STRONG_BUY":
        return rsi.iloc[-2] < 30 and rsi.iloc[-1] >= 30
    if direcao == "STRONG_SELL":
        return rsi.iloc[-2] > 70 and rsi.iloc[-1] <= 70

def validar_macd(df, direcao):
    macd = df['macd']
    signal = df['macd_signal']
    if direcao == "STRONG_BUY":
        return macd.iloc[-2] < signal.iloc[-2] and macd.iloc[-1] > signal.iloc[-1]
    if direcao == "STRONG_SELL":
        return macd.iloc[-2] > signal.iloc[-2] and macd.iloc[-1] < signal.iloc[-1]
      
