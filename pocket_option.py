from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

EMAIL = os.getenv("PO_EMAIL", "guipocketbrasil@gmail.com")
SENHA = os.getenv("PO_SENHA", "Guiladonorte633")

def obter_saldo():
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        # Usa webdriver_manager para baixar e configurar o driver
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        driver.get("https://pocketoption.com/pt/login/")
        time.sleep(4)

        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SENHA)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(6)

        driver.get("https://pocketoption.com/pt/platform/")
        time.sleep(8)

        try:
            botao = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
            botao.click()
            time.sleep(3)
        except:
            pass

        saldo_element = driver.find_element(By.CLASS_NAME, "balance-value")
        saldo_texto = saldo_element.text.strip().replace("$", "").replace(",", ".")

        print(f"[INFO] Saldo obtido: ${saldo_texto}")
        driver.quit()
        return saldo_texto

    except Exception as e:
        print(f"[ERRO] Falha ao obter saldo: {e}")
        return "Erro"
