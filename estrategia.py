from indicadores import analisar_indicadores

def verificar_estrategia(par):
    resultado = analisar_indicadores(par)

    if not resultado:
        return None

    strong = resultado.get("strong")
    sar = resultado.get("sar")
    rsi = resultado.get("rsi")
    macd = resultado.get("macd")

    if strong and sar and rsi and macd:
        direcao = "CALL" if strong == "STRONG_BUY" else "PUT"
        return {
            "par": par,
            "direcao": direcao,
            "mensagem": f"🔔 Sinal confirmado em {par} para {direcao} com todos os indicadores!"
        }

    return None
