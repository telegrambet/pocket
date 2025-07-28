import json
import os
from datetime import datetime, timedelta
from telegram_bot import send_message

ARQUIVO_JSON = "retraction_history.json"
ALERTA_MINUTOS_ANTES = 10
MINIMO_RETRACAO_PIPS = 5
DIAS_HISTORICO = 10
MINIMO_REPETICOES = 8

def carregar_historico():
    if os.path.exists(ARQUIVO_JSON):
        with open(ARQUIVO_JSON, "r") as f:
            return json.load(f)
    return {}

def salvar_historico(dados):
    with open(ARQUIVO_JSON, "w") as f:
        json.dump(dados, f, indent=2)

def registrar_retracao(horario_candle):
    hoje = datetime.now().strftime("%Y-%m-%d")
    historico = carregar_historico()

    if horario_candle not in historico:
        historico[horario_candle] = []

    # Evita duplicatas no mesmo dia
    if hoje not in historico[horario_candle]:
        historico[horario_candle].append(hoje)

    # Mantém apenas os últimos 10 dias
    for horario in historico:
        historico[horario] = historico[horario][-DIAS_HISTORICO:]

    salvar_historico(historico)

def verificar_alertas():
    agora = datetime.now()
    horario_alvo = (agora + timedelta(minutes=ALERTA_MINUTOS_ANTES)).strftime("%H:%M")
    historico = carregar_historico()

    if horario_alvo in historico:
        repeticoes = len(historico[horario_alvo])
        if repeticoes >= MINIMO_REPETICOES:
            send_message(
                f"⚠️ Alerta: possível retração às {horario_alvo} (ocorreu em {repeticoes}/10 dias)"
            )
