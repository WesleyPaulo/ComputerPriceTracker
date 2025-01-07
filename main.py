from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

driver_path = 'chromedriver.exe'
#request_url = 'https://www.terabyteshop.com.br/produto/20813/processador-amd-ryzen-7-5700x-34ghz-46ghz-turbo-8-cores-16-threads-am4-sem-cooler-100-100000926wof'
request_url = 'https://www.terabyteshop.com.br/produto/29665/monitor-gamer-ninja-tenseigan-27-pol-full-hd-ips-1ms-240hz-hdr-freesync-hdmidp-white-mgn-007-27w'

#Chrome Options
options = webdriver.ChromeOptions()
#options.add_argument("headless=new")
#options.add_argument("--disable-gpu")
#options.add_argument("--no-sandbox")
#options.add_argument("--window-size=1920x1080")
#options.add_experimental_option('excludeSwitches', ['enable-automation'])

options.add_argument("maximize_window()")

#Setup Driver
driver = webdriver.Chrome(
    options=options, service=Service(executable_path=driver_path)
)



#Requests
driver.minimize_window()
#driver.set_window_position(-10000,0)
driver.get(request_url)
wait = WebDriverWait(driver, 20)
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
time.sleep(5)


#Get Contens
product_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tit-prod'))).get_attribute("textContent")
product_cash_price = wait.until(EC.presence_of_element_located((By.ID, 'valVista'))).get_attribute("textContent")
product_card_price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'valParc'))).get_attribute("textContent")
product_card_installments_a = wait.until(EC.presence_of_element_located((By.ID, 'nParc'))).get_attribute("textContent")
product_card_installments_b = wait.until(EC.presence_of_element_located((By.ID, 'Parc'))).get_attribute("textContent")
product_card_installments = product_card_installments_a + " de " + product_card_installments_b

# Tests
print("Produto: ", product_title)
print("Preço à Vista: ", product_cash_price)
print(f"Preço em Credito: {product_card_price} em {product_card_installments}")




driver.quit()