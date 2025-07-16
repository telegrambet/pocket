from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

EMAIL = os.getenv("PO_EMAIL")
SENHA = os.getenv("PO_SENHA")

def obter_saldo():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
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
        
