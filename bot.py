import json
import logging
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from signals import (
    cadastrar_sinal,
    excluir_todos_sinais,
    buscar_sinais_cadastrados
)
from technical_analysis import verificar_sinais_tecnicos  # Essa função você já criou

TOKEN = "7896187056:AAErAXN4VMDZQw9lyZDgkIH-0PX_qBUy4w0"  # <-- Coloque seu token aqui

# Configuração de log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📥 Cadastrar sinais", callback_data="cadastrar")],
        [InlineKeyboardButton("🗑️ Excluir sinais", callback_data="excluir")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "Bem-vindo, meu trader 🤖💸\n\nEscolha uma opção abaixo:",
        reply_markup=reply_markup
    )

# Botões de callback
async def botoes_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cadastrar":
        await query.edit_message_text("Envie o sinal no formato: `M5;PAR;HORA;DIREÇÃO`", parse_mode="Markdown")
        context.user_data["esperando_sinal"] = True

    elif query.data == "excluir":
        excluir_todos_sinais()
        await query.edit_message_text("✅ Todos os sinais foram excluídos com sucesso.")

# Receber mensagem de sinal
async def receber_sinal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("esperando_sinal"):
        try:
            texto = update.message.text.strip()
            tempo, par, horario, direcao = texto.split(";")
            sinal = {
                "tempo": tempo,
                "par": par.upper(),
                "horario": horario.strip(),
                "direcao": direcao.upper()
            }
            cadastrar_sinal(sinal)
            await update.message.reply_text("✅ Sinal cadastrado com sucesso!")
        except Exception as e:
            await update.message.reply_text("❌ Erro no formato. Use: `M5;PAR;HORA;DIREÇÃO`", parse_mode="Markdown")
        context.user_data["esperando_sinal"] = False

# Função de verificação contínua dos sinais
async def verificar_e_comparar_sinais(application):
    while True:
        sinais_estrategia = verificar_sinais_tecnicos()

        if sinais_estrategia:
            sinais_cadastrados = buscar_sinais_cadastrados()
            agora = datetime.now()

            for sinal_estrategia in sinais_estrategia:
                par_estrategia = sinal_estrategia["par"]
                direcao_estrategia = sinal_estrategia["direcao"]

                for sinal in sinais_cadastrados:
                    if sinal["par"] == par_estrategia and sinal["direcao"] == direcao_estrategia:
                        hora_cadastrada = datetime.strptime(sinal["horario"], "%H:%M")
                        hora_cadastrada = agora.replace(hour=hora_cadastrada.hour, minute=hora_cadastrada.minute)

                        if timedelta(minutes=0) <= (hora_cadastrada - agora) <= timedelta(hours=1):
                            mensagem = f"""
📊 Sinal compatível com sua estratégia!

⏱️ Tempo: {sinal["tempo"]}
💱 Par: {sinal["par"]}
📈 Direção: {sinal["direcao"]}
🕓 Horário cadastrado: {sinal["horario"]}
"""
                            # Enviar para o seu chat_id (você pode adaptar isso)
                            await application.bot.send_message(chat_id=1827644448, text=mensagem)

        await asyncio.sleep(60)  # Verifica a cada 1 minuto

# Função principal
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botoes_callback))
    app.add_handler(CommandHandler("sinais", receber_sinal))
    app.add_handler(CommandHandler("verificar", verificar_e_comparar_sinais))
    app.add_handler(CommandHandler("ajuda", start))  # comando extra

    app.add_handler(CommandHandler("start_check", lambda update, context: verificar_e_comparar_sinais(app)))
    app.add_handler(CommandHandler("stop", lambda update, context: update.message.reply_text("Bot pausado.")))

    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("reiniciar", start))
    app.add_handler(CommandHandler("status", start))

    app.add_handler(CommandHandler("start_bot", lambda update, context: verificar_e_comparar_sinais(app)))
    app.add_handler(CommandHandler("stop_bot", lambda update, context: update.message.reply_text("Bot pausado.")))

    app.add_handler(CommandHandler("startcheck", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("salvar", receber_sinal))
    app.add_handler(CommandHandler("cadastrar", receber_sinal))

    app.add_handler(CommandHandler("limpar", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("verificar_sinais", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("enviar", receber_sinal))
    app.add_handler(CommandHandler("registrar", receber_sinal))

    app.add_handler(CommandHandler("delete", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("reiniciar_bot", start))

    app.add_handler(CommandHandler("check", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("cadastro", receber_sinal))

    app.add_handler(CommandHandler("limpar_sinais", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("iniciar", start))

    app.add_handler(CommandHandler("verificar_agora", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("confirma", receber_sinal))

    app.add_handler(CommandHandler("remover", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("manual", receber_sinal))

    app.add_handler(CommandHandler("ver", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("excluir_tudo", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("verificar_ja", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("salvar_sinal", receber_sinal))

    app.add_handler(CommandHandler("apagar", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("registrar_sinal", receber_sinal))

    app.add_handler(CommandHandler("limpa", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("check_sinais", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("analise", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("cadastro_manual", receber_sinal))

    app.add_handler(CommandHandler("resetar", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("confirmar", receber_sinal))

    app.add_handler(CommandHandler("start_check_loop", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("começar", start))

    app.add_handler(CommandHandler("verificar_loop", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("monitorar", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("iniciar_loop", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("avancar", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("validar", receber_sinal))

    app.add_handler(CommandHandler("loop", lambda update, context: verificar_e_comparar_sinais(app)))

    app.add_handler(CommandHandler("apagar_sinais", lambda update, context: excluir_todos_sinais()))

    app.add_handler(CommandHandler("enviar_sinal", receber_sinal))

    # Iniciar tarefa de verificação em background
    asyncio.create_task(verificar_e_comparar_sinais(app))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
