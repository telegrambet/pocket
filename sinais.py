# sinais.py
import json
from datetime import datetime, timedelta

ARQUIVO_SINAIS = "sinais_cadastrados.json"

def salvar_sinal(formato):
    try:
        timeframe, par, hora, direcao = formato.split(";")
        with open(ARQUIVO_SINAIS, "r") as f:
            sinais = json.load(f)
    except FileNotFoundError:
        sinais = []

    novo = {
        "timeframe": timeframe.strip().upper(),
        "par": par.strip().upper(),
        "hora": hora.strip(),
        "direcao": direcao.strip().upper()
    }

    sinais.append(novo)
    with open(ARQUIVO_SINAIS, "w") as f:
        json.dump(sinais, f, indent=2)

def limpar_sinais():
    with open(ARQUIVO_SINAIS, "w") as f:
        json.dump([], f)

def buscar_sinal_compatível(par, direcao):
    try:
        with open(ARQUIVO_SINAIS, "r") as f:
            sinais = json.load(f)
    except FileNotFoundError:
        return None

    agora = datetime.now()
    for sinal in sinais:
        if sinal["par"] != par.upper() or sinal["direcao"] != direcao.upper():
            continue

        hora_sinal = datetime.strptime(sinal["hora"], "%H:%M")
        hora_sinal = agora.replace(hour=hora_sinal.hour, minute=hora_sinal.minute, second=0, microsecond=0)

        if 0 <= (hora_sinal - agora).total_seconds() <= 3600:
            return sinal

    return None
