import time
import threading
from config import ATIVOS, VALORES_ENTRADA
from sinais import sinais_confirmados
from indicadores import calcular_indicadores, validar_sar, cruzou_rsi, validar_macd
from pocket_option import entrar_na_pocket_option
from controle import pode_operar
from candles import obter_candles_binance
from telegram_bot import main as iniciar_telegram, enviar_mensagem

# 🚀 Inicia o bot do Telegram em paralelo
threading.Thread(target=iniciar_telegram).start()

def obter_candles_reais(ativo):
    df = obter_candles_binance(ativo, intervalo="5m", limite=100)
    if df is not None:
        return calcular_indicadores(df)
    else:
        print(f"[ERRO] Não foi possível obter candles de {ativo}")
        return None

# 🔄 Loop principal de operação
while True:
    if pode_operar():
        for ativo in ATIVOS:
            ok, direcao = sinais_confirmados(ativo)
            if ok:
                df = obter_candles_reais(ativo)
                if df is None:
                    continue

                if validar_sar(df, direcao) and cruzou_rsi(df, direcao) and validar_macd(df, direcao):
                    payout_atual = 0.75  # ← substitua por leitura real com Selenium se quiser

                    if payout_atual < 0.70:
                        enviar_mensagem(f"⚠️ Payout de {payout_atual*100:.0f}% está abaixo do mínimo. Ignorando entrada.")
                        continue

                    valor = VALORES_ENTRADA[0]
                    enviar_mensagem(f"🎯 Entrada confirmada: {ativo} ({direcao}) no valor de ${valor}")

                    resultado = entrar_na_pocket_option(ativo, direcao, valor)

                    if resultado == "win":
                        enviar_mensagem(f"✅ Vitória direta no {ativo}! 🏆")
                    elif resultado == "loss":
                        enviar_mensagem(f"❌ Derrota na entrada no {ativo}. Tentando Gale 1...")

                        valor = VALORES_ENTRADA[1]
                        resultado = entrar_na_pocket_option(ativo, direcao, valor)

                        if resultado == "win":
                            enviar_mensagem("✅ Vitória no Gale 1! 🔁")
                        elif resultado == "loss":
                            enviar_mensagem("❌ Derrota no Gale 1. Tentando Gale 2...")

                            valor = VALORES_ENTRADA[2]
                            resultado = entrar_na_pocket_option(ativo, direcao, valor)

                            if resultado == "win":
                                enviar_mensagem("✅ Vitória no Gale 2! 💥")
                            else:
                                enviar_mensagem("❌ Derrota total, incluindo Gale 2. 🪦")
                    break
            else:
                print("Layout abaixo, procurando sinal...")
    else:
        print("Fora do horário ou bot parado.")
    time.sleep(60)
                        
