# deriv.py
import requests

# Token da API Deriv (mantenha em segredo, de preferência via variável de ambiente)
DERIV_TOKEN = 'fB3F5O5sWdS4gxg'

def get_candles(symbol, count=3, granularity=300):
    """
    Retorna candles do ativo informado na Deriv.
    
    :param symbol: string, nome do ativo (ex: R_100, R_50, etc)
    :param count: int, quantidade de candles
    :param granularity: int, tempo do candle em segundos (300 = M5)
    :return: lista de candles
    """
    url = f'https://api.deriv.com/api/exchange/v1/history?symbol={symbol}&granularity={granularity}&count={count}'
    headers = {'Authorization': f'Bearer {DERIV_TOKEN}'}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data.get('candles', [])
    except Exception as e:
        print(f"Erro ao obter candles de {symbol}: {e}")
        return []
