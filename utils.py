# pocket/utils.py

def calcular_variacao(open_price, close_price):
    return round((float(close_price) - float(open_price)) * 10000, 1)

def interpretar_movimento(variacao_pips):
    if variacao_pips >= 20:
        return "Alta", f"+{variacao_pips} pips"
    elif variacao_pips <= -20:
        return "Baixa", f"{variacao_pips} pips"
    else:
        return None, None
      
