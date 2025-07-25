# pocket/main.py

import time
from api_twelve import get_last_candle
from telegram_alert import enviar_alerta
from utils import calcular_variacao, interpretar_movimento

pares = ["EUR/USD", "EUR/GBP", "EUR/JPY", "AUD/JPY", "GBP/JPY", "EUR/CHF"]

def simbolo_twelve(par):
    return par.replace("/", "")

def analisar_pares():
    for par in pares:
        symbol = simbolo_twelve(par)
        candle_atual, candle_anterior = get_last_candle(symbol)

        if candle_atual:
            open_price = candle_atual["open"]
            close_price = candle_atual["close"]
            variacao = calcular_variacao(open_price, close_price)
            direcao, texto_pips = interpretar_movimento(variacao)

            if direcao:
                mensagem = (
                    f"🚨 *Explosão Direcional Detectada*\n\n"
                    f"📍 Par: {par}\n"
                    f"🕒 Timeframe: M15\n"
                    f"⏱️ Tempo de análise: primeiros 10 minutos do candle\n"
                    f"📈 Direção dominante: *{direcao}*\n"
                    f"📊 Velocidade: {texto_pips} em 10 minutos\n"
                    f"⏳ Tempo restante: ~5 minutos\n"
                    f"🎯 *Possível retração ou continuação forte!*"
                )
                enviar_alerta(mensagem)

if __name__ == "__main__":
    while True:
        print("Analisando pares...")
        analisar_pares()
        time.sleep(60 * 15)  # roda a cada 15 minutos
