# bot.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from signals import salvar_sinal, excluir_todos_sinais, buscar_sinais_cadastrados
from indicadores import verificar_estrategia
from datetime import datetime
import asyncio
import pytz

TOKEN = "7896187056:AAErAXN4VMDZQw9lyZDgkIH-0PX_qBUy4w0"

# === Mensagem inicial com botões ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("✅ Cadastrar sinais", callback_data="cadastrar_sinais")],
        [InlineKeyboardButton("❌ Excluir sinais", callback_data="excluir_sinais")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo meu trader 🤖💸", reply_markup=reply_markup)

# === Handler dos botões ===
async def botao_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cadastrar_sinais":
        await query.edit_message_text("Envie o sinal no formato:\n\nM5;EURUSD;14:30;CALL")
    elif query.data == "excluir_sinais":
        excluir_todos_sinais()
        await query.edit_message_text("✅ Todos os sinais foram excluídos com sucesso.")

# === Receber e salvar sinais enviados ===
async def receber_mensagem(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mensagem = update.message.text.strip().upper()

    try:
        timeframe, par, hora, direcao = mensagem.split(";")
        salvar_sinal(timeframe, par, hora, direcao)
        await update.message.reply_text("✅ Sinal cadastrado com sucesso!")
    except:
        await update.message.reply_text("❌ Formato inválido. Use: M5;EURUSD;14:30;CALL")

# === Verificador constante ===
async def verificador_constante(application):
    while True:
        sinais = buscar_sinais_cadastrados()
        agora = datetime.now(pytz.utc)

        for sinal in sinais:
            timeframe, par, hora_str, direcao = sinal
            hora_sinal = datetime.strptime(hora_str, "%H:%M").replace(
                year=agora.year, month=agora.month, day=agora.day, tzinfo=pytz.utc
            )

            # Dentro da próxima 1 hora
            if 0 <= (hora_sinal - agora).total_seconds() <= 3600:
                resultado = verificar_estrategia(par)

                if resultado["direcao"] == direcao:
                    mensagem = (
                        f"✅ SINAL CONFIRMADO\n\n"
                        f"PAR: {par}\n"
                        f"⏰ Horário: {hora_str}\n"
                        f"🧠 Estratégia: STRONG_{direcao}\n"
                        f"📊 Timeframes: Confirmados\n"
                        f"🟢 Entrada recomendada: {direcao}"
                    )

                    # Enviar para todos os administradores ou grupo
                    for chat_id in application.chat_data:
                        try:
                            await application.bot.send_message(chat_id=chat_id, text=mensagem)
                        except:
                            pass

        await asyncio.sleep(60)  # Verifica a cada minuto

# === Guardar chat_id ao interagir ===
async def salvar_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    context.application.chat_data[chat_id] = True  # Apenas salva

# === Inicializador do bot ===
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(botao_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receber_mensagem))
    app.add_handler(MessageHandler(filters.ALL, salvar_chat_id))  # Para salvar chat_id

    # Iniciar a verificação constante
    asyncio.create_task(verificador_constante(app))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
