import os
import requests
from bs4 import BeautifulSoup

SINAIS_FILE = "sinais.txt"
ALERTS_FILE = "alerts_sent.txt"

def salvar_sinais(texto):
    with open(SINAIS_FILE, "a") as f:
        for linha in texto.strip().split("\n"):
            f.write(linha.strip() + "\n")

def ler_sinais():
    if not os.path.exists(SINAIS_FILE):
        return "Nenhum sinal cadastrado."
    with open(SINAIS_FILE, "r") as f:
        return f.read()

def ler_alertas_enviados():
    if not os.path.exists(ALERTS_FILE):
        return set()
    with open(ALERTS_FILE, "r") as f:
        return set(line.strip() for line in f)

def salvar_alerta_enviado(sinal):
    with open(ALERTS_FILE, "a") as f:
        f.write(sinal + "\n")

def verificar_sinais_tecnicos():
    sinais = ler_sinais().strip().split("\n")
    resultados = []
    for sinal in sinais:
        try:
            tf, par, hora, direcao = sinal.split(";")
            investing = indicadores_investing(par)
            tradingview = indicadores_tradingview(par)
            comp_investing = "✅" if direcao.upper() in investing else "❌"
            comp_tradingview = "✅" if direcao.upper() in tradingview else "❌"
            resultados.append(
                f"{par} ({tf} - {hora} - {direcao})\n"
                f"Investing.com:\n{investing}\nCompatibilidade: {comp_investing}\n\n"
                f"TradingView:\n{tradingview}\nCompatibilidade: {comp_tradingview}\n"
                "----------------------------\n"
            )
        except Exception as e:
            resultados.append(f"⚠️ Erro ao processar sinal: {sinal} ({e})")
    return "\n".join(resultados)

def indicadores_investing(par):
    par_formatado = par.upper().replace("/", "")
    url = f"https://br.investing.com/technical/{par_formatado}-technical-summary"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")

        timeframes = ['5 minutos', '15 minutos', '1 hora']
        resultado = []

        for tf in timeframes:
            el = soup.find("td", string=tf)
            if el:
                valor = el.find_next("td").text.strip()
                resultado.append(f"{tf}: {valor}")
        return "\n".join(resultado)
    except Exception as e:
        return f"Erro Investing.com: {e}"

def indicadores_tradingview(par):
    par_formatado = par.upper()
    url = f"https://pt.tradingview.com/symbols/{par_formatado}/technicals/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, "html.parser")

        resumo = soup.find("div", {"class": "speedometerWrapper-1o9iH5Uz"})
        if resumo:
            texto = resumo.get_text(separator="\n").strip()
            return texto
        else:
            elementos = soup.find_all("div", {"class": "speedometerSignal-3KyfA7B9"})
            if elementos:
                textos = [el.get_text() for el in elementos]
                return "\n".join(textos)
        return "Resumo técnico não encontrado"
    except Exception as e:
        return f"Erro TradingView: {e}"
