from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import time
import updater
import database



#Initialize database
class database_creator:
    
    driver_path = ''
    data_path = ''
    db = ''
    
    def __init__(self, driver_path, data_path, db):
        self.driver_path = driver_path
        self.data_path = data_path
        self.db = db
    
    def creator(self):
        with open(self.data_path, 'r') as archive:
            for request in archive:
                if not request.startswith('#'):
                    driver = webdriver.Chrome(service=Service(executable_path=self.driver_path))
                    print(request)
                    ecommerce = request.split('.')[1].split('.')[0]

                    #Requests
                    #driver.set_window_position(-10000,0)
                    driver.minimize_window()
                    driver.get(request)
                    wait = WebDriverWait(driver, 20)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(10)


                    #Get Contents Terabyte
                    product_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tit-prod'))).get_attribute("textContent")
                    self.db.add(product_title, request, ecommerce)
                    driver.quit()
        self.db.commit()