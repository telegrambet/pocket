from datetime import datetime, timedelta

def format_retracao_extra(message):
    linhas = message.splitlines()
    par = linhas[0].replace("📍", "").strip()
    direcao_texto = linhas[1]
    hora_agora = datetime.now()

    # Arredondar minuto para o próximo múltiplo de 5
    minuto = (hora_agora.minute // 5 + 1) * 5
    if minuto == 60:
        hora_agora += timedelta(hours=1)
        minuto = 0
    horario_formatado = hora_agora.replace(minute=minuto, second=0).strftime("%H:%M")

    if "ALTA" in direcao_texto.upper():
        direcao = "CALL"
    elif "BAIXA" in direcao_texto.upper():
        direcao = "PUT"
    else:
        direcao = "DESCONHECIDO"

    return f"M5;{par};{horario_formatado};{direcao}"
