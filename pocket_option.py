from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Dados de login (use variáveis de ambiente no Railway para segurança!)
import os
EMAIL = os.getenv("PO_EMAIL", "guipocketbrasil@gmail.com")
SENHA = os.getenv("PO_SENHA", "Guiladonorte633")

def obter_saldo():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pocketoption.com/pt/login/")
        time.sleep(4)

        # Faz login
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SENHA)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(6)

        # Acessa painel de operações
        driver.get("https://pocketoption.com/pt/platform/")
        time.sleep(8)

        # Tenta trocar para conta real (caso esteja na demo)
        try:
            conta_elemento = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
            conta_elemento.click()
            time.sleep(3)
        except:
            pass  # já está na conta real ou não foi necessário

        # Captura saldo
        saldo_element = driver.find_element(By.CLASS_NAME, "balance-value")
        saldo_texto = saldo_element.text.strip().replace("$", "").replace(",", ".")

        print(f"[INFO] Saldo obtido: ${saldo_texto}")
        driver.quit()
        return saldo_texto

    except Exception as e:
        print(f"[ERRO] Falha ao obter saldo: {e}")
        return "Erro"
        
