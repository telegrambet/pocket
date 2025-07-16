from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Substitua por variáveis de ambiente se desejar
EMAIL = "guipocketbrasil@gmail.com"
SENHA = "Guiladonorte633"

def obter_saldo():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pocketoption.com/pt/login/")
        time.sleep(3)

        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SENHA)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        driver.get("https://pocketoption.com/pt/platform/")
        time.sleep(5)

        try:
            botao_conta_real = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
            botao_conta_real.click()
            time.sleep(2)
        except:
            pass

        saldo_element = driver.find_element(By.CLASS_NAME, "balance-value")
        saldo = saldo_element.text.strip().replace("$", "").replace(",", ".")
        driver.quit()
        return saldo

    except Exception as e:
        print(f"[ERRO] Falha ao obter saldo: {e}")
        return "Erro"

def entrar_na_pocket_option(par, direcao, valor):
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pocketoption.com/pt/login/")
        time.sleep(3)

        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SENHA)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)

        driver.get("https://pocketoption.com/pt/platform/")
        time.sleep(5)

        try:
            botao_conta_real = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
            botao_conta_real.click()
            time.sleep(2)
        except:
            pass

        # Seleciona o ativo (par de moedas)
        driver.find_element(By.CLASS_NAME, "asset-select-button").click()
        time.sleep(1)
        campo_pesquisa = driver.find_element(By.XPATH, "//input[@placeholder='Pesquisar']")
        campo_pesquisa.send_keys(par)
        time.sleep(1)
        driver.find_element(By.XPATH, f"//div[contains(text(), '{par}')]").click()
        time.sleep(2)

        # Define valor da entrada
        campo_valor = driver.find_element(By.CLASS_NAME, "amount-input")
        campo_valor.clear()
        campo_valor.send_keys(str(valor))
        time.sleep(1)

        # Clica no botão de CALL ou PUT
        if direcao.upper() == "CALL":
            driver.find_element(By.CLASS_NAME, "btn-up").click()
        elif direcao.upper() == "PUT":
            driver.find_element(By.CLASS_NAME, "btn-down").click()

        time.sleep(3)  # tempo para confirmar a entrada
        driver.quit()
        print(f"[ENTRADA] {par} - {direcao} - ${valor}")
    except Exception as e:
        print(f"[ERRO] Falha na entrada: {e}")
