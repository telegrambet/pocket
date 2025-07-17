# main.py

import asyncio
from signals import buscar_sinais_cadastrados
from indicadores import verificar_estrategia
from telegram_bot import enviar_alerta
from datetime import datetime, timedelta

pares_monitorados = ["EURUSD", "EURJPY", "EURGBP", "GBPJPY", "USDJPY"]

async def verificar_sinais():
    while True:
        agora = datetime.utcnow()
        sinais = buscar_sinais_cadastrados()

        for sinal in sinais:
            timeframe, par, hora_str, direcao = sinal
            hora_sinal = datetime.strptime(hora_str, "%H:%M").replace(
                year=agora.year, month=agora.month, day=agora.day
            )

            if 0 <= (hora_sinal - agora).total_seconds() <= 3600:
                if par in pares_monitorados:
                    resultado = verificar_estrategia(par)

                    if resultado["direcao"] == direcao:
                        mensagem = (
                            f"✅ SINAL CONFIRMADO\n\n"
                            f"PAR: {par}\n"
                            f"⏰ Horário: {hora_str}\n"
                            f"🧠 Estratégia: STRONG_{direcao}\n"
                            f"📊 Timeframes: Confirmados\n"
                            f"🟢 Entrada recomendada: {direcao}"
                        )
                        await enviar_alerta(mensagem)

        await asyncio.sleep(60)  # Espera 1 minuto para a próxima checagem

if __name__ == "__main__":
    asyncio.run(verificar_sinais())
