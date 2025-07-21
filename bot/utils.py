# bot/utils.py
import requests
from bs4 import BeautifulSoup

def get_tradingview_indicators(pair):
    # Simulação de acesso ao TradingView (pode ser adaptado com API real se tiver acesso)
    # Aqui você colocaria o scraping real ou API
    return {
        "RSI": "Neutral",
        "MACD": "Cruzando para cima",
        "Estocástico": "Cruzando para cima",
        "Parabolic SAR": "CALL"
    }

def get_investing_signal(pair):
    try:
        url = f"https://br.investing.com/technical/personalized-quotes-technical-summary"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Aqui você pode ajustar para buscar o par específico
        # Esta parte pode precisar ser adaptada com base na estrutura real da página

        return {
            "5M": "COMPRA FORTE",
            "15M": "COMPRA",
            "1H": "NEUTRO"
        }
    except Exception as e:
        print(f"[ERRO - Investing] {e}")
        return None
