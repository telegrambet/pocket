import json
import os
from datetime import datetime, timedelta
import pytz

RET_PATH = "retracoes.json"
RET_PIPS = 5
RET_DIAS = 10
PARES = [
    "frxEURUSD", "frxEURJPY", "frxGBPJPY", "frxUSDJPY",
    "frxCADJPY", "frxAUDCAD", "frxEURCHF", "frxEURAUD"
]

# ============ UTILS ============

def carregar_json():
    if os.path.exists(RET_PATH):
        with open(RET_PATH, "r") as f:
            return json.load(f)
    return {}

def salvar_json(dados):
    with open(RET_PATH, "w") as f:
        json.dump(dados, f, indent=2)

def hora_padrao(dt=None):
    if dt is None:
        dt = datetime.now(pytz.timezone("America/Sao_Paulo"))
    return dt.strftime("%H:%M")

def arredondar_para_m5(dt):
    minuto = (dt.minute // 5) * 5
    return dt.replace(minute=minuto, second=0, microsecond=0)

# ============ PRINCIPAL ============

def analisar_retracao(par, candle):
    open = float(candle["open"])
    close = float(candle["close"])
    high = float(candle["high"])
    low = float(candle["low"])

    direcao = "call" if close > open else "put"
    corpo = abs(close - open)
    pavio = (high - low) - corpo

    retraiu = False
    if direcao == "put" and (high - max(open, close)) * 10000 >= RET_PIPS:
        retraiu = True
    elif direcao == "call" and (min(open, close) - low) * 10000 >= RET_PIPS:
        retraiu = True

    return retraiu, direcao

def registrar_retracao(par, horario):
    dados = carregar_json()
    if par not in dados:
        dados[par] = {}
    if horario not in dados[par]:
        dados[par][horario] = []

    hoje = datetime.now().strftime("%Y-%m-%d")
    if hoje not in dados[par][horario]:
        dados[par][horario].append(hoje)
        # manter apenas os últimos 10 dias
        dados[par][horario] = dados[par][horario][-RET_DIAS:]
        salvar_json(dados)

def verificar_alertas():
    agora = datetime.now(pytz.timezone("America/Sao_Paulo"))
    horario_alvo = (agora + timedelta(minutes=10)).strftime("%H:%M")

    dados = carregar_json()
    sinais = []
    for par in dados:
        for horario in dados[par]:
            if horario == horario_alvo and len(dados[par][horario]) >= RET_DIAS:
                sinais.append((par, horario))

    return sinais

# ============ INTEGRAR COM SEU LOOP ============

def processar_candle(par, candle):
    dt = datetime.fromtimestamp(candle["epoch"], pytz.timezone("America/Sao_Paulo"))
    dt_m5 = arredondar_para_m5(dt)
    horario = dt_m5.strftime("%H:%M")

    retraiu, direcao = analisar_retracao(par, candle)
    if retraiu:
        registrar_retracao(par, horario)
        print(f"[✓] {par} | {horario} | {direcao.upper()} teve retração!")

def enviar_alertas(bot):
    sinais = verificar_alertas()
    for par, horario in sinais:
        msg = f"📉 SINAL DE RETRAÇÃO 📉\n\nPar: {par}\nHorário: {horario}\nCondição: Candle M5 com retração nos últimos 10 dias consecutivos.\n\n⏱️ Prepare-se!"
        bot.send_message(chat_id=SEU_CHAT_ID, text=msg)
  
