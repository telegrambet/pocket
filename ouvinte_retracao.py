from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime, timedelta
import re

# Função que deve ser chamada em seu Application.add_handler(...)
async def processar_retracao(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    texto = update.message.text

    # Verifica se é uma mensagem de retração
    if "POSSÍVEL RETRAÇÃO DE ALTA" in texto or "POSSÍVEL RETRAÇÃO DE BAIXA" in texto:
        # Extrai o par de moedas da primeira linha
        linhas = texto.split('\n')
        par = None
        for linha in linhas:
            if "📍" in linha:
                par_match = re.search(r"📍\s*(\w+)", linha)
                if par_match:
                    par = par_match.group(1)

        if not par:
            return  # não achou o par de moedas

        # Direção
        direcao = "CALL" if "ALTA" in texto else "PUT"

        # Hora futura ajustada para múltiplos de 5
        agora = datetime.now()
        minuto = ((agora.minute // 5) + 1) * 5
        proximo_horario = agora.replace(minute=0, second=0, microsecond=0) + timedelta(minutes=minuto)

        hora_formatada = proximo_horario.strftime("%H:%M")

        mensagem_formatada = f"M5;{par};{hora_formatada};{direcao}"

        await update.message.reply_text(mensagem_formatada)
                  
