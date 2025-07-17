import time
from datetime import datetime
from estrategia import verificar_estrategia
from sinais import buscar_sinais_compativeis

pares = ["EURUSD", "EURJPY", "EURGBP", "GBPJPY", "USDJPY"]

def executar_verificacao():
    while True:
        agora = datetime.now().strftime("%H:%M")

        for par in pares:
            resultado = verificar_estrategia(par)
            if resultado:
                compativeis = buscar_sinais_compativeis(par, resultado["direcao"], agora)
                if compativeis:
                    print(f"\n🔔 SINAL COMPATÍVEL DETECTADO")
                    print(resultado["mensagem"])
                    print("🕒 Horário atual:", agora)
                    print("📌 Sinais cadastrados compatíveis:")
                    for sinal in compativeis:
                        print("👉", sinal)

        time.sleep(60)  # Verifica a cada 1 minuto
