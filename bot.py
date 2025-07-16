import time
import threading
from config import ATIVOS, VALORES_ENTRADA
from sinais import sinais_confirmados
from indicadores import calcular_indicadores, validar_sar, cruzou_rsi, validar_macd
from pocket_option import entrar_na_pocket_option
from controle import pode_operar
from candles import obter_candles_binance
from telegram_bot import main as iniciar_telegram  # Bot Telegram

# 🔁 Obter candles reais e calcular indicadores
def obter_candles_reais(ativo):
    df = obter_candles_binance(ativo, intervalo="5m", limite=100)
    if df is not None:
        return calcular_indicadores(df)
    else:
        print(f"[ERRO] Não foi possível obter candles reais de {ativo}")
        return None

# 🚀 Inicia o bot do Telegram em paralelo
threading.Thread(target=iniciar_telegram).start()

# 🔄 Loop principal do robô
while True:
    if pode_operar():
        for ativo in ATIVOS:
            ok, direcao = sinais_confirmados(ativo)
            if ok:
                df = obter_candles_reais(ativo)
                if df is None:
                    continue  # pula esse ativo se deu erro ao buscar candles

                if validar_sar(df, direcao) and cruzou_rsi(df, direcao) and validar_macd(df, direcao):
                    valor = VALORES_ENTRADA[0]  # $3
                    entrar_na_pocket_option(ativo, direcao, valor)
                    print("Bom dia Trader, estamos em operação 💸🤖")
                    break  # uma única entrada por loop
            else:
                print("Layout abaixo, procurando sinal...")
    else:
        print("Fora do horário ou bot parado.")
    time.sleep(60)
    
