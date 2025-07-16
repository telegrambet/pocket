from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

# Seus dados de login (importante: use variáveis de ambiente no Railway depois!)
EMAIL = "guipocketbrasil@gmail.com"
SENHA = "Guiladonorte633"

def obter_saldo():
    try:
        # Configura navegador invisível
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://pocketoption.com/pt/login/")

        # Espera o carregamento da página de login
        time.sleep(3)

        # Preenche e envia login
        driver.find_element(By.NAME, "email").send_keys(EMAIL)
        driver.find_element(By.NAME, "password").send_keys(SENHA)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()

        # Espera o redirecionamento
        time.sleep(5)

        # Vai para o painel
        driver.get("https://pocketoption.com/pt/platform/")

        # Espera o painel carregar
        time.sleep(5)

        # Seleciona a conta real (evita saldo de demo)
        try:
            botao_conta_real = driver.find_element(By.XPATH, "//span[contains(text(), 'Conta real')]")
            botao_conta_real.click()
            time.sleep(2)
        except:
            pass  # já pode estar na conta real

        # Encontra o saldo no topo
        saldo_element = driver.find_element(By.CLASS_NAME, "balance-value")
        saldo = saldo_element.text.strip().replace("$", "").replace(",", ".")

        driver.quit()
        return saldo

    except Exception as e:
        print(f"[ERRO] Falha ao obter saldo: {e}")
        return "Erro"

