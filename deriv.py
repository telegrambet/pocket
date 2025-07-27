# deriv.py
import requests

DERIV_TOKEN = 'fB3F5O5sWdS4gxg'

def get_candles(symbol, count=3, granularity=300):
    url = 'https://api.deriv.com/websockets/v3'
    payload = {
        'ticks_history': symbol,
        'style': 'candles',
        'granularity': granularity,
        'count': count,
        'end': 'latest',
        'subscribe': 0,
        'req_id': 1
    }

    headers = {'Authorization': f'Bearer {DERIV_TOKEN}'}
    try:
        response = requests.get(f'https://api.deriv.com/api/exchange/v1/history?symbol={symbol}&granularity={granularity}&count={count}', headers=headers)
        data = response.json()
        return data.get('candles', [])
    except Exception as e:
        print(f\"Erro ao obter candles de {symbol}: {e}\")
        return []
              
