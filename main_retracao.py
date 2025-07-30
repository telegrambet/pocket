import asyncio
from datetime import datetime
import pytz
from deriv import get_candles
from retration import processar_candle, verificar_alertas
from telegram_bot import send_alert, send_welcome

PAIRS = ["frxEURUSD", "frxEURJPY", "frxEURGBP", "frxUSDJPY", "frxGBPJPY"]
CHECK_INTERVAL = 180  # 3 minutos
TIMEZONE = pytz.timezone("America/Sao_Paulo")

def is_retraction_window():
    now = datetime.now(TIMEZONE)
    return now.minute % 5 in [0,1,2,3]

async def enviar_alertas_retracao():
    sinais = verificar_alertas()
    for par, horario in sinais:
        msg = f"📉 SINAL DE RETRAÇÃO 📉\n\nPar: {par}\nHorário: {horario}\nCondição: Candle M5 com retração por 10 dias consecutivos.\n\n⏱️ Prepare-se!"
        await send_alert(msg)

async def monitor_retracao():
    await send_welcome()
    print("✅ Monitor de retração iniciado...")
    while True:
        if is_retraction_window():
            for par in PAIRS:
                candles = get_candles(par)
                if candles:
                    ultimo_candle = candles[-1]
                    processar_candle(par, ultimo_candle)
            await enviar_alertas_retracao()
        else:
            print("⏳ Fora da janela de retração. Aguardando...")
        await asyncio.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    asyncio.run(monitor_retracao())



main retração está assim! Portanto não mecha em nada, apenas adicione está função !!
