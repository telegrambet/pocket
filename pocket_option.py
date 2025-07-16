from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

EMAIL = os.getenv("PO_EMAIL", "guipocketbrasil@gmail.com")
SENHA = os.getenv("PO_SENHA", "Guiladonorte633")

def iniciar_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def login_pocket_option(driver):
    driver.get("https://pocketoption.com/pt/login/")
    time.sleep(5)

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(SENHA)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(7)

    driver.get("https://pocketoption.com/pt/platform/")
    time.sleep(10)

    try:
        botao = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
        botao.click()
        time.sleep(3)
    except:
        pass

def obter_saldo():
    try:
        driver = iniciar_driver()
        login_pocket_option(driver)

        saldo_element = driver.find_element(By.CLASS_NAME, "balance-value")
        saldo_texto = saldo_element.text.strip().replace("$", "").replace(",", ".")

        print(f"[INFO] Saldo obtido: ${saldo_texto}")
        driver.quit()
        return saldo_texto

    except Exception as e:
        print(f"[ERRO] Falha ao obter saldo: {e}")
        return "Erro"

def entrar_na_pocket_option(ativo, direcao, valor):
    try:
        driver = iniciar_driver()
        login_pocket_option(driver)

        print(f"[ENTRADA] Ativo: {ativo} | Direção: {direcao} | Valor: ${valor}")

        # Seleciona o ativo
        time.sleep(3)
        campo_ativo = driver.find_element(By.CLASS_NAME, "asset-select")
        campo_ativo.click()
        time.sleep(2)
        busca = driver.find_element(By.CLASS_NAME, "search")
        busca.send_keys(ativo)
        time.sleep(2)
        driver.find_element(By.XPATH, f"//div[contains(text(), '{ativo}')]").click()
        time.sleep(3)

        # Expiração 5 minutos
        tempo_exp = driver.find_element(By.CLASS_NAME, "timer-value")
        tempo_exp.click()
        time.sleep(1)
        driver.find_element(By.XPATH, "//span[contains(text(), '5 minutos')]").click()
        time.sleep(2)

        # Valor da entrada
        input_valor = driver.find_element(By.CLASS_NAME, "amount-input")
        input_valor.clear()
        input_valor.send_keys(str(valor))
        time.sleep(2)

        # Entrada CALL ou PUT
        if direcao == "STRONG_BUY":
            driver.find_element(By.CLASS_NAME, "deal__rise").click()
        elif direcao == "STRONG_SELL":
            driver.find_element(By.CLASS_NAME, "deal__fall").click()

        print("[✅] Entrada executada com sucesso.")
        time.sleep(3)
        driver.quit()

    except Exception as e:
        print(f"[ERRO] Falha ao executar entrada: {e}")
        
