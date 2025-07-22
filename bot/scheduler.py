import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from telegram.constants import ParseMode
from telegram.ext import ApplicationBuilder
from bot.utils import ler_sinais, indicadores_investing, indicadores_tradingview, ler_alertas_enviados, salvar_alerta_enviado

def start_scheduler(app):
    scheduler = AsyncIOScheduler()
    app.bot_data["running"] = True

    async def job_check_signals():
        if not app.bot_data.get("running", True):
            return

        sinais = ler_sinais().strip().split("\n")
        alerts_sent = ler_alertas_enviados()
        chat_id = app.bot_data.get("chat_id")

        for sinal in sinais:
            if sinal in alerts_sent:
                continue
            try:
                tf, par, hora, direcao = sinal.split(";")
                investing = indicadores_investing(par)
                tradingview = indicadores_tradingview(par)
                # Checagem simplificada: compatível se direcao está em qualquer resultado
                compat_investing = direcao.upper() in investing
                compat_tradingview = direcao.upper() in tradingview

                if compat_investing and compat_tradingview:
                    texto = (
                        f"🚨 Sinal confirmado 🚨\n\n"
                        f"{par} ({tf} - {hora} - {direcao})\n\n"
                        f"Investing.com:\n{investing}\n\n"
                        f"TradingView:\n{tradingview}\n"
                    )
                    if chat_id:
                        await app.bot.send_message(chat_id=chat_id, text=texto, parse_mode=ParseMode.MARKDOWN)
                        salvar_alerta_enviado(sinal)
            except Exception:
                continue

    scheduler.add_job(lambda: asyncio.create_task(job_check_signals()), "interval", minutes=5)
    scheduler.start()
