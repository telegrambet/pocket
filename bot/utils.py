import os
import requests
from bs4 import BeautifulSoup

# Simula banco simples
SINAIS_FILE = "sinais.txt"

def salvar_sinais(texto):
    with open(SINAIS_FILE, "a") as f:
        for linha in texto.strip().split("\n"):
            f.write(linha.strip() + "\n")

def ler_sinais():
    if not os.path.exists(SINAIS_FILE):
        return "Nenhum sinal cadastrado."
    with open(SINAIS_FILE, "r") as f:
        return f.read()

def verificar_sinais_tecnicos():
    sinais = ler_sinais().strip().split("\n")
    resultados = []
    for sinal in sinais:
        try:
            tf, par, hora, direcao = sinal.split(";")
            indicadores = status_indicadores(par)
            compatibilidade = "✅ Compatível" if direcao in indicadores else "❌ Não compatível"
            resultados.append(f"{par} ({tf} - {hora} - {direcao})\n{indicadores}\n{compatibilidade}\n")
        except:
            resultados.append(f"⚠️ Erro ao processar sinal: {sinal}")
    return "\n".join(resultados)

def status_indicadores(par):
    par_formatado = par.upper().replace("/", "")
    url = f"https://br.investing.com/technical/{par_formatado}-technical-summary"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        r = requests.get(url, headers=headers)
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
        return f"Erro ao buscar indicadores: {e}"
