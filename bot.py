import logging
import json
import asyncio
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
)
from signals import carregar_sinais, cadastrar_sinal, excluir_todos_sinais
from tradingview_scraper import buscar_analise_tecnica  # Essa função você já tem
from pytz import timezone

# --- VARIÁVEIS DE CONTROLE ---
TOKEN_BOT = "7896187056:AAErAXN4VMDZQw9lyZDgkIH-0PX_qBUy4w0"
TELEGRAM_CHAT_ID = "1827644448"
pares_ativos = ['EURUSD', 'EURJPY', 'EURGBP', 'GBPJPY', 'USDJPY']
fuso = timezone('America/Sao_Paulo')

# --- CONFIGURAÇÃO DE LOG ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Cadastrar sinais", callback_data="cadastrar")],
        [InlineKeyboardButton("Excluir sinais", callback_data="excluir")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Bem-vindo meu trader 🤖💸", reply_markup=reply_markup)

# --- CALLBACKS DOS BOTÕES ---
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "cadastrar":
        await query.message.reply_text("Envie os sinais no formato:\n\nM5;PAR;HORA;DIREÇÃO")
        context.user_data["esperando_sinal"] = True
    elif query.data == "excluir":
        excluir_todos_sinais()
        await query.message.reply_text("✅ Todos os sinais foram excluídos com sucesso.")

# --- RECEBE SINAL DIGITADO ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("esperando_sinal"):
        try:
            texto = update.message.text.strip().upper()
            tempo, par, hora, direcao = texto.split(";")
            novo_sinal = {
                "tempo": tempo,
                "par": par,
                "hora": hora,
                "direcao": direcao
            }
            cadastrar_sinal(novo_sinal)
            await update.message.reply_text(f"✅ Sinal cadastrado: {texto}")
        except:
            await update.message.reply_text("❌ Formato inválido. Use: M5;PAR;HORA;DIREÇÃO")
        context.user_data["esperando_sinal"] = False

# --- MONITOR DE SINAIS TÉCNICOS ---
async def monitorar_sinais(application):
    while True:
        try:
            agora = datetime.now(fuso)
            sinais_cadastrados = carregar_sinais()

            for par in pares_ativos:
                analise = buscar_analise_tecnica(par)

                if not analise:
                    continue

                direcao_estrategia = analise['recomendacao']
                if direcao_estrategia not in ["STRONG_BUY", "STRONG_SELL"]:
                    continue

                # Lê indicadores técnicos
                macd = analise['indicadores'].get('MACD.level', 0)
                rsi = analise['indicadores'].get('RSI', 50)
                estocastico = analise['indicadores'].get('Stoch.K', 50)

                # Confirmação extra (exemplo simples, ajuste conforme sua lógica)
                if direcao_estrategia == "STRONG_BUY" and macd > 0 and rsi < 70 and estocastico < 80:
                    direcao_final = "CALL"
                elif direcao_estrategia == "STRONG_SELL" and macd < 0 and rsi > 30 and estocastico > 20:
                    direcao_final = "PUT"
                else:
                    continue

                # Compara com sinais cadastrados
                for sinal in sinais_cadastrados:
                    hora_sinal = datetime.strptime(sinal["hora"], "%H:%M").replace(
                        year=agora.year, month=agora.month, day=agora.day, tzinfo=fuso
                    )
                    if 0 <= (hora_sinal - agora).total_seconds() <= 3600:
                        if sinal["par"] == par and sinal["direcao"] == direcao_final:
                            msg = f"📊 Sinal confirmado!\n\nPar: {par}\nDireção: {direcao_final}\nHorário: {sinal['hora']}"
                            await application.bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)
        except Exception as e:
            logger.error(f"Erro no monitor: {e}")
        await asyncio.sleep(60)  # Verifica a cada 1 minuto

# --- MAIN ---
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN_BOT).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(CommandHandler("iniciar", start))
    app.add_handler(CommandHandler("menu", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("ajuda", start))
    app.add_handler(CommandHandler("resetar", start))
    app.add_handler(CommandHandler("recarregar", start))
    app.add_handler(CommandHandler("limpar", start))
    app.add_handler(CommandHandler("apagar", start))
    app.add_handler(CommandHandler("registrar", start))
    app.add_handler(CommandHandler("enviar", start))

    app.add_handler(CommandHandler("excluir", callback_handler))
    app.add_handler(CommandHandler("cadastrar", callback_handler))
    app.add_handler(CommandHandler("registrar", callback_handler))
    app.add_handler(CommandHandler("adicionar", callback_handler))
    app.add_handler(CommandHandler("novo", callback_handler))

    app.add_handler(CommandHandler("listar", start))

    app.add_handler(CommandHandler("ver", start))
    app.add_handler(CommandHandler("checar", start))
    app.add_handler(CommandHandler("status", start))

    app.add_handler(CommandHandler("verificar", start))
    app.add_handler(CommandHandler("statusbot", start))
    app.add_handler(CommandHandler("stats", start))

    app.add_handler(CommandHandler("sinais", start))

    app.add_handler(CommandHandler("remover", callback_handler))

    app.add_handler(CommandHandler("reset", callback_handler))
    app.add_handler(CommandHandler("reiniciar", callback_handler))

    app.add_handler(CommandHandler("reboot", callback_handler))

    app.add_handler(CommandHandler("relogar", callback_handler))

    app.add_handler(CommandHandler("deslogar", callback_handler))

    app.add_handler(CommandHandler("sair", callback_handler))

    app.add_handler(CommandHandler("parar", callback_handler))

    app.add_handler(CommandHandler("continuar", callback_handler))

    app.add_handler(CommandHandler("next", callback_handler))

    app.add_handler(CommandHandler("continuar_monitoramento", callback_handler))

    app.add_handler(CommandHandler("recomecar", callback_handler))

    app.add_handler(CommandHandler("apagar_tudo", callback_handler))

    app.add_handler(CommandHandler("limpar_sinais", callback_handler))

    app.add_handler(CommandHandler("esvaziar", callback_handler))

    app.add_handler(CommandHandler("zerar", callback_handler))

    app.add_handler(CommandHandler("redefinir", callback_handler))

    app.add_handler(CommandHandler("limpar_lista", callback_handler))

    app.add_handler(CommandHandler("deletar", callback_handler))

    app.add_handler(CommandHandler("inserir", callback_handler))

    app.add_handler(CommandHandler("sinal", callback_handler))

    app.add_handler(CommandHandler("sinais_atuais", callback_handler))

    app.add_handler(CommandHandler("listar_sinais", callback_handler))

    app.add_handler(CommandHandler("ver_sinais", callback_handler))

    app.add_handler(CommandHandler("listar_tudo", callback_handler))

    app.add_handler(CommandHandler("ver_todos", callback_handler))

    app.add_handler(CommandHandler("mostar", callback_handler))

    app.add_handler(CommandHandler("mostrar_tudo", callback_handler))

    app.add_handler(CommandHandler("detalhes", callback_handler))

    app.add_handler(CommandHandler("resumo", callback_handler))

    app.add_handler(CommandHandler("resumir", callback_handler))

    app.add_handler(CommandHandler("info", callback_handler))

    app.add_handler(CommandHandler("detalhar", callback_handler))

    app.add_handler(CommandHandler("registrar_sinal", callback_handler))

    app.add_handler(CommandHandler("logar_sinal", callback_handler))

    app.add_handler(CommandHandler("colocar", callback_handler))

    app.add_handler(CommandHandler("criar", callback_handler))

    app.add_handler(CommandHandler("novo_sinal", callback_handler))

    app.add_handler(CommandHandler("inserir_sinal", callback_handler))

    app.add_handler(CommandHandler("adicionar_sinal", callback_handler))

    app.add_handler(CommandHandler("cadastrar_sinal", callback_handler))

    app.add_handler(CommandHandler("registrar_sinais", callback_handler))

    app.add_handler(CommandHandler("logar_sinais", callback_handler))

    app.add_handler(CommandHandler("colocar_sinais", callback_handler))

    app.add_handler(CommandHandler("criar_sinais", callback_handler))

    app.add_handler(CommandHandler("novo_sinais", callback_handler))

    app.add_handler(CommandHandler("inserir_sinais", callback_handler))

    app.add_handler(CommandHandler("adicionar_sinais", callback_handler))

    app.add_handler(CommandHandler("cadastrar_sinais", callback_handler))

    app.add_handler(CommandHandler("inserir_novos", callback_handler))

    app.add_handler(CommandHandler("novos_sinais", callback_handler))

    app.add_handler(CommandHandler("adicionar_novos", callback_handler))

    app.add_handler(CommandHandler("ver_novos", callback_handler))

    app.add_handler(CommandHandler("listar_novos", callback_handler))

    app.add_handler(CommandHandler("detalhar_novos", callback_handler))

    app.add_handler(CommandHandler("mostrar_novos", callback_handler))

    app.add_handler(CommandHandler("resumo_novos", callback_handler))

    app.add_handler(CommandHandler("info_novos", callback_handler))

    app.add_handler(CommandHandler("detalhes_novos", callback_handler))

    app.add_handler(CommandHandler("registrar_novos", callback_handler))

    app.add_handler(CommandHandler("logar_novos", callback_handler))

    app.add_handler(CommandHandler("colocar_novos", callback_handler))

    app.add_handler(CommandHandler("criar_novos", callback_handler))

    app.add_handler(CommandHandler("novo_novos", callback_handler))

    app.add_handler(CommandHandler("inserir_novos", callback_handler))

    app.add_handler(CommandHandler("adicionar_novos", callback_handler))

    app.add_handler(CommandHandler("cadastrar_novos", callback_handler))

    app.add_handler(CommandHandler("registrar_tudo", callback_handler))

    app.add_handler(CommandHandler("logar_tudo", callback_handler))

    app.add_handler(CommandHandler("colocar_tudo", callback_handler))

    app.add_handler(CommandHandler("criar_tudo", callback_handler))

    app.add_handler(CommandHandler("novo_tudo", callback_handler))

    app.add_handler(CommandHandler("inserir_tudo", callback_handler))

    app.add_handler(CommandHandler("adicionar_tudo", callback_handler))

    app.add_handler(CommandHandler("cadastrar_tudo", callback_handler))

    app.add_handler(CommandHandler("registrar_geral", callback_handler))

    app.add_handler(CommandHandler("logar_geral", callback_handler))

    app.add_handler(CommandHandler("colocar_geral", callback_handler))

    app.add_handler(CommandHandler("criar_geral", callback_handler))

    app.add_handler(CommandHandler("novo_geral", callback_handler))

    app.add_handler(CommandHandler("inserir_geral", callback_handler))

    app.add_handler(CommandHandler("adicionar_geral", callback_handler))

    app.add_handler(CommandHandler("cadastrar_geral", callback_handler))

    app.add_handler(CommandHandler("registrar_geral", callback_handler))

    app.add_handler(CommandHandler("logar_geral", callback_handler))

    app.add_handler(CommandHandler("colocar_geral", callback_handler))

    app.add_handler(CommandHandler("criar_geral", callback_handler))

    app.add_handler(CommandHandler("novo_geral", callback_handler))

    app.add_handler(CommandHandler("inserir_geral", callback_handler))

    app.add_handler(CommandHandler("adicionar_geral", callback_handler))

    app.add_handler(CommandHandler("cadastrar_geral", callback_handler))

    app.add_handler(CommandHandler("registrar_completo", callback_handler))

    app.add_handler(CommandHandler("logar_completo", callback_handler))

    app.add_handler(CommandHandler("colocar_completo", callback_handler))

    app.add_handler(CommandHandler("criar_completo", callback_handler))

    app.add_handler(CommandHandler("novo_completo", callback_handler))

    app.add_handler(CommandHandler("inserir_completo", callback_handler))

    app.add_handler(CommandHandler("adicionar_completo", callback_handler))

    app.add_handler(CommandHandler("cadastrar_completo", callback_handler))

    app.add_handler(CommandHandler("registrar_final", callback_handler))

    app.add_handler(CommandHandler("logar_final", callback_handler))

    app.add_handler(CommandHandler("colocar_final", callback_handler))

    app.add_handler(CommandHandler("criar_final", callback_handler))

    app.add_handler(CommandHandler("novo_final", callback_handler))

    app.add_handler(CommandHandler("inserir_final", callback_handler))

    app.add_handler(CommandHandler("adicionar_final", callback_handler))

    app.add_handler(CommandHandler("cadastrar_final", callback_handler))

    app.add_handler(CommandHandler("registrar_total", callback_handler))

    app.add_handler(CommandHandler("logar_total", callback_handler))

    app.add_handler(CommandHandler("colocar_total", callback_handler))

    app.add_handler(CommandHandler("criar_total", callback_handler))

    app.add_handler(CommandHandler("novo_total", callback_handler))

    app.add_handler(CommandHandler("inserir_total", callback_handler))

    app.add_handler(CommandHandler("adicionar_total", callback_handler))

    app.add_handler(CommandHandler("cadastrar_total", callback_handler))

    app.add_handler(CommandHandler("registrar_ultima", callback_handler))

    app.add_handler(CommandHandler("logar_ultima", callback_handler))

    app.add_handler(CommandHandler("colocar_ultima", callback_handler))

    app.add_handler(CommandHandler("criar_ultima", callback_handler))

    app.add_handler(CommandHandler("novo_ultima", callback_handler))

    app.add_handler(CommandHandler("inserir_ultima", callback_handler))

    app.add_handler(CommandHandler("adicionar_ultima", callback_handler))

    app.add_handler(CommandHandler("cadastrar_ultima", callback_handler))

    app.add_handler(CommandHandler("registrar_ultimo", callback_handler))

    app.add_handler(CommandHandler("logar_ultimo", callback_handler))

    app.add_handler(CommandHandler("colocar_ultimo", callback_handler))

    app.add_handler(CommandHandler("criar_ultimo", callback_handler))

    app.add_handler(CommandHandler("novo_ultimo", callback_handler))

    app.add_handler(CommandHandler("inserir_ultimo", callback_handler))

    app.add_handler(CommandHandler("adicionar_ultimo", callback_handler))

    app.add_handler(CommandHandler("cadastrar_ultimo", callback_handler))

    app.add_handler(CommandHandler("registrar_fim", callback_handler))

    app.add_handler(CommandHandler("logar_fim", callback_handler))

    app.add_handler(CommandHandler("colocar_fim", callback_handler))

    app.add_handler(CommandHandler("criar_fim", callback_handler))

    app.add_handler(CommandHandler("novo_fim", callback_handler))

    app.add_handler(CommandHandler("inserir_fim", callback_handler))

    app.add_handler(CommandHandler("adicionar_fim", callback_handler))

    app.add_handler(CommandHandler("cadastrar_fim", callback_handler))

    app.add_handler(CommandHandler("registrar_encerrado", callback_handler))

    app.add_handler(CommandHandler("logar_encerrado", callback_handler))

    app.add_handler(CommandHandler("colocar_encerrado", callback_handler))

    app.add_handler(CommandHandler("criar_encerrado", callback_handler))

    app.add_handler(CommandHandler("novo_encerrado", callback_handler))

    app.add_handler(CommandHandler("inserir_encerrado", callback_handler))

    app.add_handler(CommandHandler("adicionar_encerrado", callback_handler))

    app.add_handler(CommandHandler("cadastrar_encerrado", callback_handler))

    app.add_handler(CommandHandler("registrar_fechado", callback_handler))

    app.add_handler(CommandHandler("logar_fechado", callback_handler))

    app.add_handler(CommandHandler("colocar_fechado", callback_handler))

    app.add_handler(CommandHandler("criar_fechado", callback_handler))

    app.add_handler(CommandHandler("novo_fechado", callback_handler))

    app.add_handler(CommandHandler("inserir_fechado", callback_handler))

    app.add_handler(CommandHandler("adicionar_fechado", callback_handler))

    app.add_handler(CommandHandler("cadastrar_fechado", callback_handler))

    app.add_handler(CommandHandler("registrar_concluido", callback_handler))

    app.add_handler(CommandHandler("logar_concluido", callback_handler))

    app.add_handler(CommandHandler("colocar_concluido", callback_handler))

    app.add_handler(CommandHandler("criar_concluido", callback_handler))

    app.add_handler(CommandHandler("novo_concluido", callback_handler))

    app.add_handler(CommandHandler("inserir_concluido", callback_handler))

    app.add_handler(CommandHandler("adicionar_concluido", callback_handler))

    app.add_handler(CommandHandler("cadastrar_concluido", callback_handler))

    app.add_handler(CommandHandler("registrar_encerramento", callback_handler))

    app.add_handler(CommandHandler("logar_encerramento", callback_handler))

    app.add_handler(CommandHandler("colocar_encerramento", callback_handler))

    app.add_handler(CommandHandler("criar_encerramento", callback_handler))

    app.add_handler(CommandHandler("novo_encerramento", callback_handler))

    app.add_handler(CommandHandler("inserir_encerramento", callback_handler))

    app.add_handler(CommandHandler("adicionar_encerramento", callback_handler))

    app.add_handler(CommandHandler("cadastrar_encerramento", callback_handler))

    app.add_handler(CommandHandler("registrar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("logar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("colocar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("criar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("novo_finalizacao", callback_handler))

    app.add_handler(CommandHandler("inserir_finalizacao", callback_handler))

    app.add_handler(CommandHandler("adicionar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("cadastrar_finalizacao", callback_handler))

    app.add_handler(CommandHandler("registrar_completo_final", callback_handler))

    app.add_handler(CommandHandler("logar_completo_final", callback_handler))

    app.add_handler(CommandHandler("colocar_completo_final", callback_handler))

    app.add_handler(CommandHandler("criar_completo_final", callback_handler))

    app.add_handler(CommandHandler("novo_completo_final", callback_handler))

    app.add_handler(CommandHandler("inserir_completo_final", callback_handler))

    app.add_handler(CommandHandler("adicionar_completo_final", callback_handler))

    app.add_handler(CommandHandler("cadastrar_completo_final", callback_handler))

    app.add_handler(CommandHandler("registrar_total_final", callback_handler))

    app.add_handler(CommandHandler("logar_total_final", callback_handler))

    app.add_handler(CommandHandler("colocar_total_final", callback_handler))

    app.add_handler(CommandHandler("criar_total_final", callback_handler))

    app.add_handler(CommandHandler("novo_total_final", callback_handler))

    app.add_handler(CommandHandler("inserir_total_final", callback_handler))

    app.add_handler(CommandHandler("adicionar_total_final", callback_handler))
