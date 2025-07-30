import requests
import time
import json
from datetime import datetime, timedelta

# === Configurações ===
PAIRS = ["frxEURUSD", "frxEURJPY", "frxEURGBP", "frxUSDJPY", "frxGBPJPY"]
GRANULARITY_M5 = 300
GRANULARITY_M1 = 60
RETRACAO_PIPS = 5
DIAS_ANALISE = 10
HORARIOS_REPETICAO = 7
ARQUIVO_SAIDA = "horarios_retracao.json"

# === Função para puxar candles ===
def puxar_candles(par, granularidade, fim_epoca, quantidade):
    url = f"https://api.binary.com/v3/pricehistory?symbol={par}&granularity={granularidade}&end={fim_epoca}&count={quantidade}"
    r = requests.get(url)
    data = r.json()
    return data["candles"] if "candles" in data else []

# === Verifica retração nos 2 minutos finais do candle M5 ===
def verificar_retracao(candle_m5, par):
    timestamp = candle_m5["epoch"]
    open_price = candle_m5["open"]
    close_price = candle_m5["close"]
    direcao = "CALL" if close_price < open_price else "PUT"

    # pega os 2 últimos minutos do candle
    fim_m5 = timestamp + 300
    m1_candles = puxar_candles(par, GRANULARITY_M1, fim_m5, 5)

    if len(m1_candles) < 5:
        return None

    ultimos_2 = m1_candles[-2:]
    m1_pips = abs(ultimos_2[0]["close"] - ultimos_2[1]["close"]) * 100000

    if direcao == "CALL" and ultimos_2[0]["close"] > ultimos_2[1]["close"] and m1_pips >= RETRACAO_PIPS:
        return "CALL"
    elif direcao == "PUT" and ultimos_2[0]["close"] < ultimos_2[1]["close"] and m1_pips >= RETRACAO_PIPS:
        return "PUT"
    return None

# === Função principal para analisar os últimos 10 dias ===
def detectar_retracoes():
    resultado = {}

    for par in PAIRS:
        print(f"\n🔍 Analisando par: {par}")
        horarios = {}

        for dias_atras in range(1, DIAS_ANALISE + 1):
            dia = datetime.utcnow() - timedelta(days=dias_atras)
            fim_dia = int(datetime(dia.year, dia.month, dia.day, 23, 59).timestamp())
            candles_m5 = puxar_candles(par, GRANULARITY_M5, fim_dia, 300)

            for c in candles_m5:
                dt = datetime.utcfromtimestamp(c["epoch"])
                minuto = dt.minute
                if minuto % 5 != 0:
                    continue  # ignora candles fora do fechamento exato de 5 em 5 minutos

                hora_formatada = dt.strftime("%H:%M")
                direcao = verificar_retracao(c, par)

                if direcao:
                    if hora_formatada not in horarios:
                        horarios[hora_formatada] = {"CALL": 0, "PUT": 0}
                    horarios[hora_formatada][direcao] += 1

                time.sleep(0.15)  # para evitar ban da API

        # Seleciona horários que ocorreram 7x ou mais
        resultado[par] = []
        for hora, dados in horarios.items():
            for direcao, contagem in dados.items():
                if contagem >= HORARIOS_REPETICAO:
                    resultado[par].append({"hora": hora, "direcao": direcao})
                    print(f"✔️ {hora} - {direcao} ({contagem}x)")

    with open(ARQUIVO_SAIDA, "w") as f:
        json.dump(resultado, f, indent=2)

    print(f"\n✅ Análise finalizada! Resultados salvos em: {ARQUIVO_SAIDA}")
    return resultado

# === Executa ao rodar direto ===
if __name__ == "__main__":
    detectar_retracoes()
