# estrutura de arquivos:
# - bot.py               → comando Telegram
# - estrategia.py        → verifica STRONG_BUY/SELL + SAR + RSI + MACD
# - sinais.py            → gerencia os sinais cadastrados
# - verificador.py       → checa a estratégia e envia alerta se houver sinal compatível

# ==========================
# arquivo: sinais.py
# ==========================
import json
import os
from datetime import datetime, timedelta

ARQUIVO_SINAIS = 'sinais.json'

# cria o arquivo se não existir
def inicializar_arquivo():
    if not os.path.exists(ARQUIVO_SINAIS):
        with open(ARQUIVO_SINAIS, 'w') as f:
            json.dump([], f)

# cadastra novo sinal
def cadastrar_sinal(texto):
    try:
        tempo, par, hora, direcao = texto.split(';')
        sinal = {
            'tempo': tempo,
            'par': par.upper(),
            'hora': hora.strip(),
            'direcao': direcao.upper(),
        }
        with open(ARQUIVO_SINAIS, 'r+') as f:
            sinais = json.load(f)
            sinais.append(sinal)
            f.seek(0)
            json.dump(sinais, f, indent=2)
        return True
    except:
        return False

# limpa todos os sinais
def excluir_sinais():
    with open(ARQUIVO_SINAIS, 'w') as f:
        json.dump([], f)

# retorna lista de sinais válidos (com horário até 1h na frente)
def buscar_sinais_compatíveis(par, direcao):
    agora = datetime.now()
    sinais_compatíveis = []
    with open(ARQUIVO_SINAIS, 'r') as f:
        sinais = json.load(f)
        for sinal in sinais:
            if sinal['par'] == par and sinal['direcao'] == direcao:
                hora_sinal = datetime.strptime(sinal['hora'], '%H:%M')
                hora_sinal = agora.replace(hour=hora_sinal.hour, minute=hora_sinal.minute, second=0)
                if 0 <= (hora_sinal - agora).total_seconds() <= 3600:
                    sinais_compatíveis.append(sinal)
    return sinais_compatíveis
        
from tradingview_ta import TA_Handler, Interval

def obter_recomendacao(ativo, timeframe):
    handler = TA_Handler(
        symbol=ativo,
        screener="forex",
        exchange="FX_IDC",
        interval=timeframe
    )
    return handler.get_analysis().summary['RECOMMENDATION']

def sinais_confirmados(ativo):
    timeframes = [
        Interval.INTERVAL_4_HOURS,
        Interval.INTERVAL_1_HOUR,
        Interval.INTERVAL_15_MINUTES,
        Interval.INTERVAL_5_MINUTES
    ]
    sinais = [obter_recomendacao(ativo, tf) for tf in timeframes]
    return all(s == sinais[0] and s in ["STRONG_BUY", "STRONG_SELL"] for s in sinais), sinais[0]
  
