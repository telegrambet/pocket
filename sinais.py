import json
from datetime import datetime, timedelta

CAMINHO_SINAIS = "sinais_cadastrados.json"

def cadastrar_sinal(sinal: str) -> str:
    try:
        with open(CAMINHO_SINAIS, "r") as f:
            sinais = json.load(f)
    except FileNotFoundError:
        sinais = []

    sinais.append(sinal)
    with open(CAMINHO_SINAIS, "w") as f:
        json.dump(sinais, f, indent=4)

    return "✅ Sinal cadastrado com sucesso!"

def excluir_sinais() -> str:
    with open(CAMINHO_SINAIS, "w") as f:
        json.dump([], f)
    return "⚠️ Todos os sinais foram excluídos."

def buscar_sinais_compativeis(par: str, direcao: str, horario_base: str):
    try:
        with open(CAMINHO_SINAIS, "r") as f:
            sinais = json.load(f)
    except FileNotFoundError:
        return []

    hora_base = datetime.strptime(horario_base, "%H:%M")
    sinais_compativeis = []

    for sinal in sinais:
        try:
            tf, par_sinal, hora_sinal, direcao_sinal = sinal.split(";")
            hora_sinal_dt = datetime.strptime(hora_sinal, "%H:%M")
            diferenca = (hora_sinal_dt - hora_base).total_seconds() / 60
            if par.upper() == par_sinal.upper() and direcao.upper() == direcao_sinal.upper():
                if 0 <= diferenca <= 60:
                    sinais_compativeis.append(sinal)
        except:
            continue

    return sinais_compativeis
