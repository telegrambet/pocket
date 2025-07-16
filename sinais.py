
from tradingview_ta import TA_Handler, Interval

def obter_recomendacao(ativo, timeframe):
    handler = TA_Handler(
        symbol=ativo,
        screener="forex",
        exchange="FX_IDC",
        interval=timeframe
    )
    return handler.get_analysis().summary['RECOMMENDATION']

def sinais_confirmados(ativo):
    timeframes = [
        Interval.INTERVAL_4_HOURS,
        Interval.INTERVAL_1_HOUR,
        Interval.INTERVAL_15_MINUTES,
        Interval.INTERVAL_5_MINUTES
    ]
    sinais = [obter_recomendacao(ativo, tf) for tf in timeframes]
    return all(s == sinais[0] and s in ["STRONG_BUY", "STRONG_SELL"] for s in sinais), sinais[0]
  
