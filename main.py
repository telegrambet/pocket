# main.py
import asyncio
from datetime import datetime

from utils import PAIRS, check_retraction_signal
from deriv import get_candles
from telegram_bot import send_alert, send_welcome
from retration import detect_retraction  # <- Import da nova função

CHECK_INTERVAL = 180  # 3 minutos

def is_retraction_window():
    """
    Retorna True se o horário atual estiver dentro da janela de retração (ex: 00-03, 05-08, etc.)
    """
    minute = datetime.now().minute
    return (minute % 5) in [0, 1, 2, 3]

async def monitor():
    while True:
        print("🔍 Verificando sinais...")

        # Verifica repetição de retração dos últimos 10 dias
        detect_retraction()

        if is_retraction_window():
            for symbol, average_pips in PAIRS.items():
                candles = get_candles(symbol)
                if candles:
                    result = check_retraction_signal(symbol, candles, average_pips)
                    if result:
                        await send_alert(result)
        else:
            print("⏳ Fora da janela de retração. Aguardando...")

        await asyncio.sleep(CHECK_INTERVAL)

async def main():
    await send_welcome()
    print("✅ Bot iniciado e monitorando sinais...")
    await monitor()

if __name__ == "__main__":
    asyncio.run(main())
