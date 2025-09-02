# main.py
import asyncio
from fibonacci import check_fibonacci_touch
from utils import PAIRS
from deriv import get_candles
from telegram_bot import send_alert, send_welcome
from utils import check_retraction_signal
from datetime import datetime, timedelta
import pytz  # <--- import pytz para fuso horário

CHECK_INTERVAL = 180  # 3 minutos

def is_retraction_window():
    # Aqui pode continuar usando datetime.now(), mas cuidado com o fuso do servidor
    minute = datetime.now().minute
    return (minute % 5) == 3

def gerar_sinal_formatado(symbol: str, direcao_frase: str) -> str:
    # Direção do sinal
    if "baixa" in direcao_frase.lower():
        direcao = "PUT"
    elif "alta" in direcao_frase.lower():
        direcao = "CALL"
    else:
        direcao = "DESCONHECIDA"

    # Obtém a hora UTC atual e converte para horário de Brasília
    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    agora = utc_now.astimezone(brasilia_tz)

    # Arredonda para o próximo múltiplo de 5 minutos
    minuto = ((agora.minute // 5) + 1) * 5 - 1 
    if minuto == 60:
        proximo_horario = agora.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
    else:
        proximo_horario = agora.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minuto)

    hora_formatada = proximo_horario.strftime("%H:%M")

    # Remove "frx" apenas para exibição
    symbol_formatado = symbol.replace("frx", "")

    return f"M1;{symbol_formatado};{hora_formatada};{direcao}"


async def monitor():
    while True:
        if is_retraction_window():
            for symbol, average_pips in PAIRS.items():
                candles = get_candles(symbol)
                if candles:
                    result = check_retraction_signal(symbol, candles, average_pips)
                    if result:
                        await send_alert(result)

                        # Gerar e enviar frase no formato M5;PAR;HORA;DIREÇÃO
                        frase_sinal = gerar_sinal_formatado(symbol, result)
                        await send_alert(frase_sinal)
        else:
            print("⏳ Fora da janela de retração. Aguardando...")
        await asyncio.sleep(CHECK_INTERVAL)

async def run():
    while True:
        for pair in PAIRS.keys():
            fib_signal = check_fibonacci_touch(pair)
            if fib_signal:
                await send_alert(fib_signal)

        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    await send_welcome()
    print("✅ Bot iniciado e monitorando sinais...")
    await monitor()

if __name__ == "__main__":
    asyncio.run(main())
