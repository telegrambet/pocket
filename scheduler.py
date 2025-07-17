import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from indicadores import verificar_estrategia
from sinais import comparar_com_sinais_cadastrados
from telegram import Bot
from config import TOKEN

bot = Bot(token=TOKEN)

async def tarefa_de_verificacao():
    sinais_confirmados = await verificar_estrategia()

    for sinal in sinais_confirmados:
        alerta = comparar_com_sinais_cadastrados(sinal)
        if alerta:
            await bot.send_message(chat_id='SEU_CHAT_ID_AQUI', text=alerta)

def iniciar_agendamento(app):
    scheduler = AsyncIOScheduler(timezone="America/Sao_Paulo")
    scheduler.add_job(tarefa_de_verificacao, 'interval', minutes=1)
    scheduler.start()
