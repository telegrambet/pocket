import random

def analisar_indicadores(par):
    # Simulação dos valores: troque aqui com dados reais se quiser
    sinais_possiveis = ["STRONG_BUY", "STRONG_SELL", "BUY", "SELL", None]
    rsi_valores = [25, 32, 45, 70, 75]
    macd_ok = [True, False]

    strong = random.choice(sinais_possiveis)
    sar = random.choice([True, False])
    rsi = random.choice(rsi_valores)
    macd = random.choice(macd_ok)

    if strong not in ["STRONG_BUY", "STRONG_SELL"]:
        return None

    direcao = "CALL" if strong == "STRONG_BUY" else "PUT"

    rsi_valido = (rsi <= 30 and direcao == "CALL") or (rsi >= 70 and direcao == "PUT")

    return {
        "strong": strong,
        "sar": sar,
        "rsi": rsi_valido,
        "macd": macd
    }

# ✅ Função exigida pelo signals.py
def verificar_estrategia(par):
    resultado = analisar_indicadores(par)
    if resultado:
        if resultado["sar"] and resultado["rsi"] and resultado["macd"]:
            return "CALL" if resultado["strong"] == "STRONG_BUY" else "PUT"
    return None
