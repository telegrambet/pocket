import time
import pandas as pd
import threading
from config import ATIVOS, VALORES_ENTRADA
from sinais import sinais_confirmados
from indicadores import calcular_indicadores, validar_sar, cruzou_rsi, validar_macd
from pocket_option import entrar_na_pocket_option
from controle import pode_operar
from telegram_bot import main as iniciar_telegram  # Inicia bot Telegram

# Função temporária usando candles fictícios (substitua por candles reais depois)
def obter_candles_ficticios():
    df = pd.DataFrame({
        'open': [1.0]*10,
        'high': [1.1]*10,
        'low': [0.9]*10,
        'close': [1.0]*8 + [1.02, 1.04]
    })
    return calcular_indicadores(df)

# Inicia o bot do Telegram em segundo plano
threading.Thread(target=iniciar_telegram).start()

# Loop principal de operação
while True:
    if pode_operar():
        for ativo in ATIVOS:
            ok, direcao = sinais_confirmados(ativo)
            if ok:
                df = obter_candles_ficticios()  # <-- aqui depois você vai usar candles reais
                if validar_sar(df, direcao) and cruzou_rsi(df, direcao) and validar_macd(df, direcao):
                    valor = VALORES_ENTRADA[0]  # valor de entrada base (3$)
                    entrar_na_pocket_option(ativo, direcao, valor)
                    print("Bom dia Trader, estamos em operação 💸🤖")
                    break  # evita múltiplas entradas seguidas
            else:
                print("Layout abaixo, procurando sinal...")
    else:
        print("Fora do horário ou bot parado.")
    time.sleep(60)
