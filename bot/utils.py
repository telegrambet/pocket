import requests
from bs4 import BeautifulSoup

# Lista para armazenar sinais manualmente
sinais = []

def cadastrar_sinal(par, direcao):
    sinais.append({
        "par": par,
        "direcao": direcao
    })
    return f"Sinal cadastrado: {par} - {direcao}"

def listar_sinais():
    if not sinais:
        return "Nenhum sinal cadastrado."
    return "\n".join([f"{s['par']} - {s['direcao']}" for s in sinais])

def consultar_sinais_tecnicos():
    resposta = ""
    for sinal in sinais:
        par = sinal["par"]
        direcao = sinal["direcao"]

        indicadores = get_tradingview_indicators(par)
        investing = get_investing_signal(par)

        resposta += f"\n📊 {par} ({direcao})\n"
        if investing:
            resposta += f"5M: {investing.get('5M')}\n15M: {investing.get('15M')}\n1H: {investing.get('1H')}\n"
        else:
            resposta += "Erro ao obter sinais do Investing.com\n"

        resposta += f"\nRSI: {indicadores['RSI']}\nMACD: {indicadores['MACD']}\n"
        resposta += f"Estocástico: {indicadores['Estocástico']}\nParabolic SAR: {indicadores['Parabolic SAR']}\n"
        resposta += "-"*30 + "\n"

    return resposta if resposta else "Nenhum sinal cadastrado para consultar."

# Indicadores simulados (adaptável para API ou scraping real)
def get_tradingview_indicators(pair):
    return {
        "RSI": "Neutral",
        "MACD": "Cruzando para cima",
        "Estocástico": "Cruzando para cima",
        "Parabolic SAR": "CALL"
    }

# Sinais do Investing.com (simulado — você pode melhorar o scraping)
def get_investing_signal(pair):
    try:
        url = f"https://br.investing.com/technical/personalized-quotes-technical-summary"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Esta parte deve ser adaptada para obter o par desejado.
        return {
            "5M": "COMPRA FORTE",
            "15M": "COMPRA",
            "1H": "NEUTRO"
        }
    except Exception as e:
        print(f"[ERRO - Investing] {e}")
        return None
