import json
import os

CAMINHO_ARQUIVO_SINAIS = "sinais_cadastrados.json"

def carregar_sinais():
    if os.path.exists(CAMINHO_ARQUIVO_SINAIS):
        with open(CAMINHO_ARQUIVO_SINAIS, "r") as f:
            return json.load(f)
    else:
        return []

def salvar_sinais(sinais):
    with open(CAMINHO_ARQUIVO_SINAIS, "w") as f:
        json.dump(sinais, f, indent=4)

def cadastrar_sinal(novo_sinal):
    sinais = carregar_sinais()
    sinais.append(novo_sinal)
    salvar_sinais(sinais)

def excluir_todos_sinais():
    salvar_sinais([])

def buscar_sinais_cadastrados():
    return carregar_sinais()
