from datetime import datetime
import pytz

bot_ativo = True  # alternado por Start/Stop
zona = pytz.timezone("America/Sao_Paulo")

def dentro_do_horario():
    agora = datetime.now(zona)
    return agora.weekday() < 5 and 6 <= agora.hour < 11

def pode_operar():
    return bot_ativo and dentro_do_horario()
  
