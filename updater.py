from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
from datetime import date

class updater:
    
    driver_path = ''
    data_path = ''
    db = ''
    
    def __init__(self, driver_path, data_path, db):
        self.driver_path = driver_path
        self.data_path = data_path
        self.db = db
        
    def update(self):

        #Create columns name with the date and the type of info
        date_today = date.today().strftime('%d/%m/%Y')
        print(date_today)
        
        #Read all data in the .txt, get info in the sites and store at the database(db) 
        with open(self.data_path, 'r') as archive:
            for request in archive:
                if not request.startswith('#'):
                    driver = webdriver.Chrome(service=Service(executable_path=self.driver_path))
                    ecommerce = request.split('.')[1].split('.')[0]

                    #Requests
                    #driver.set_window_position(-10000,0)
                    driver.minimize_window()
                    driver.get(request)
                    wait = WebDriverWait(driver, 20)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(10)


                    #Get Contens Terabyte
                    print(request)
                    print(ecommerce)
                    if ecommerce == 'terabyteshop':
                        product_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tit-prod'))).get_attribute("textContent")
                        product_cash_price = wait.until(EC.presence_of_element_located((By.ID, 'valVista'))).get_attribute("textContent")
                        product_card_price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'valParc'))).get_attribute("textContent")
                        product_card_installments_a = wait.until(EC.presence_of_element_located((By.ID, 'nParc'))).get_attribute("textContent")
                        product_card_installments_b = wait.until(EC.presence_of_element_located((By.ID, 'Parc'))).get_attribute("textContent")
                        product_card_installments_c = wait.until(EC.presence_of_element_located((By.ID, 'jrParc'))).get_attribute("textContent")
                        product_card_installments = product_card_installments_a + " de " + product_card_installments_b + " " + product_card_installments_c

                    print(product_title)
                    #Get item id by product
                    #item_id = self.db.get_id_by_product(product_title)

                    #Update all new columns with the prices
                    self.db.add(product_title, request, ecommerce, product_cash_price, product_card_price, product_card_installments, date_today)

                    driver.quit()
                    
                    
        self.db.commit()
