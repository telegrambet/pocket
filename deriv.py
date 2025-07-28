# deriv.py
import json
import websocket

def get_candles(symbol, count=3, granularity=300):
    """
    Retorna candles do ativo informado via WebSocket da Deriv.

    :param symbol: string, nome do ativo (ex: frxEURJPY, frxGBPJPY)
    :param count: int, quantidade de candles (ex: 3)
    :param granularity: int, tempo do candle em segundos (300 = M5)
    :return: lista de candles ou []
    """
    try:
        # Conexão com o WebSocket oficial da Deriv
        ws = websocket.create_connection("wss://ws.binaryws.com/websockets/v3?app_id=1089")

        # Requisição em formato JSON para obter candles
        request = {
            "ticks_history": symbol,
            "start": 1,
            "end": "latest",
            "style": "candles",
            "granularity": granularity,
            "count": count
        }

        ws.send(json.dumps(request))  # Envia a requisição
        response = ws.recv()  # Recebe a resposta
        ws.close()  # Fecha a conexão

        data = json.loads(response)

        if "candles" in data:
            return data["candles"]
        else:
            print(f"[ERRO] Resposta inválida da Deriv para {symbol}: {data}")
            return []

    except Exception as e:
        print(f"Erro ao obter candles de {symbol}: {e}")
        return []
