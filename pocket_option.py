from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

EMAIL = "guipocketbrasil@gmail.com"
SENHA = "Guiladonorte633"

def entrar_na_pocket_option(ativo, direcao, valor):
    options = Options()
    # options.add_argument("--headless")  # deixe comentado se quiser ver o navegador
    driver = webdriver.Chrome(options=options)

    driver.get("https://pocketoption.com/")
    time.sleep(5)

    driver.find_element(By.NAME, "email").send_keys(EMAIL)
    driver.find_element(By.NAME, "password").send_keys(SENHA)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    time.sleep(10)  # aguarda login

    print(f"[ENTRADA] {ativo} | {direcao} | ${valor}")
    driver.quit()
  
