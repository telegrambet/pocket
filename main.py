# main.py
import time
import asyncio
from utils import PAIRS
from deriv import get_candles
from telegram_bot import send_alert
from utils import check_retraction_signal

CHECK_INTERVAL = 180  # 3 minutos

async def monitor():
    while True:
        for symbol, average_pips in PAIRS.items():
            candles = get_candles(symbol)
            if candles:
                result = check_retraction_signal(symbol, candles, average_pips)
                if result:
                    await send_alert(result)
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    print("✅ Bot iniciado e monitorando sinais...")
    asyncio.run(monitor())
