# pocket/main.py

import time
from datetime import datetime, timedelta
from api_twelve import get_candle_data
from alert_telegram import enviar_alerta
from utils import calcular_pips, tempo_restante_candle

# Pares a serem monitorados
PARES = ['EUR/USD', 'EUR/GBP', 'EUR/JPY', 'AUD/JPY', 'GBP/JPY', 'EUR/CHF']

# Parâmetros
TIMEFRAME = '15min'
INTERVALO_ANALISE = 600  # 10 minutos em segundos
LIMITE_PIPS = 20         # Explosão mínima em pips

def monitorar_explosao():
    print("🚨 Iniciando monitoramento de explosão direcional...")

    while True:
        for par in PARES:
            print(f"⏳ Analisando {par}...")

            candles = get_candle_data(par, TIMEFRAME, 2)
            if not candles or len(candles) < 2:
                print(f"❌ Erro ao buscar candles de {par}")
                continue

            candle_atual = candles[0]
            horario_inicio = datetime.strptime(candle_atual['datetime'], "%Y-%m-%d %H:%M:%S")
            agora = datetime.utcnow()

            # Verifica se já passou pelo menos 10 minutos
            if (agora - horario_inicio).total_seconds() < INTERVALO_ANALISE:
                continue

            preco_abertura = float(candle_atual['open'])
            preco_atual = float(candle_atual['close'])
            direcao = "Alta" if preco_atual > preco_abertura else "Baixa"

            pips = calcular_pips(preco_abertura, preco_atual, par)

            if abs(pips) >= LIMITE_PIPS:
                tempo_restante = tempo_restante_candle(horario_inicio, agora, 900)  # 15 min = 900s

                msg = f"""
🚨 Explosão Direcional Detectada

📍 Par: {par.replace('/', '')}
🕒 Timeframe: M15
⏱️ Tempo de análise: primeiros 10 minutos do candle
📈 Direção dominante: {direcao}
📊 Velocidade: {pips:+.1f} pips em 10 minutos
⏳ Tempo restante no candle: {tempo_restante} minutos
🎯 Possível retração ou continuação forte!
                """.strip()

                enviar_alerta(msg)
                time.sleep(2)

        time.sleep(60)  # Aguarda antes de reiniciar o loop

if __name__ == "__main__":
    monitorar_explosao()
