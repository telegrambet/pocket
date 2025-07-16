import requests
import pandas as pd

# Converte os pares para formato aceito na Binance (ex: EURUSD → EURUSDT)
CONVERSAO_BINANCE = {
    "EURUSD": "EURUSDT",
    "EURJPY": "EURJPY",
    "EURGBP": "EURGBP",
    "GBPJPY": "GBPJPY",
    "USDJPY": "USDJPY"
}

def obter_candles_binance(ativo: str, intervalo="5m", limite=100):
    if ativo not in CONVERSAO_BINANCE:
        raise ValueError(f"Par de moedas '{ativo}' não suportado.")

    simbolo = CONVERSAO_BINANCE[ativo]
    url = f"https://api.binance.com/api/v3/klines?symbol={simbolo}&interval={intervalo}&limit={limite}"

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()

        df = pd.DataFrame(dados, columns=[
            "open_time", "open", "high", "low", "close", "volume",
            "close_time", "quote_asset_volume", "number_of_trades",
            "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"
        ])

        # Apenas colunas OHLC, convertidas para float
        df = df[["open", "high", "low", "close"]].astype(float)
        return df

    except Exception as e:
        print(f"[ERRO] Falha ao obter candles: {e}")
        return None
      
