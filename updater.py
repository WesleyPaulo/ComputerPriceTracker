from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import sys
from datetime import date
from concurrent.futures import ThreadPoolExecutor
import random
import re

class updater:
    
    driver_path = ''
    data_path = ''
    db = ''
    
    def __init__(self, driver_path, data_path, db):
        self.driver_path = driver_path
        self.data_path = data_path
        self.db = db
        
    def update(self):

        #Read all data in the .txt, get info in the sites and store at the database(db) 
        with open(self.data_path, 'r') as archive:
            
            #Creates a Thread pool with five workers 
            with ThreadPoolExecutor(max_workers=5) as executor:
                for request in archive:
                    executor.submit(self.getter, request)
                    
                #Only after all the links get requesteds the commit happens 
                connection = ''   
                connection = self.db.get_connection()    
                self.db.commit(connection)  
                self.db.quit(connection)       
            
            
    def getter(self, request):
        #Ignores the lines that starts with # (comments in the .txt)
        if not request.startswith('#'):
            
            #Create columns name with the date and the type of info
            date_today = date.today().strftime('%d/%m/%Y')
            
            #Get the name of the E-commerce
            ecommerce = request.split('.')[1].split('.')[0]
            """if ecommerce == "terabyteshop":
                return None
            if ecommerce == "kabum":
                return None"""
            
            #Initializes the driver
            options = webdriver.ChromeOptions()
            #options.add_argument("--headless=new")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("start-maximized")
            options.add_argument("disable-infobars")
            driver = webdriver.Chrome(service=Service(executable_path=self.driver_path), options=options)
            driver.set_window_position(-10000, 0)
            

            #Request, waits a random time(the scroll is for all the site can be loaded) 
            #driver.minimize_window()
            driver.get(request)
            wait = WebDriverWait(driver, random.randint(10,20))


            #Get Contents of Terabyteshop
            print(ecommerce)
            if ecommerce == 'terabyteshop':
                #If the title can't be found the site has been changed or the URL is incorrect 
                try: 
                    product_title = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'tit-prod'))).get_attribute("textContent")
                except:
                    print("Error with product: can't find the product. Link: ", request)
                    pass
                
                #If the Code can't be found the site has been changed or the URL is incorrect      
                try:
                    code = wait.until(EC.presence_of_element_located((By.ID, "partnumber"))).get_attribute("textContent")
                    result = re.search(r'CÓD:\s*(.+)$', code)
                    product_code = result.group(1)
                except Exception as e:
                    print("Error with product: can't find the product model. Link: " + request + " .Error: " + e )
                    pass
                
                #If don't have the cash price the product is unavailable
                try:
                    product_cash_price = wait.until(EC.presence_of_element_located((By.ID, 'valVista'))).get_attribute("textContent")
                except:
                    product_cash_price = ""
                    
                #If don't have the card price the price is the same as the cash price
                try:
                    product_card_price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'valParc'))).get_attribute("textContent")
                except:
                    product_card_price = product_cash_price
                    
                #If don't have the installments the product can't be purchased with cards
                try:
                    product_card_installments_a = wait.until(EC.presence_of_element_located((By.ID, 'nParc'))).get_attribute("textContent")
                    product_card_installments_b = wait.until(EC.presence_of_element_located((By.ID, 'Parc'))).get_attribute("textContent")
                    product_card_installments_c = wait.until(EC.presence_of_element_located((By.ID, 'jrParc'))).get_attribute("textContent")
                    product_card_installments = product_card_installments_a + " de " + product_card_installments_b + " " + product_card_installments_c
                except:
                    product_card_installments = ""
                
                    
            
            if ecommerce == 'kabum':
                #If the title can't be found the site has been changed or the URL is incorrect 
                try: 
                    product_title = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-58b2114e-6.brTtKt'))).get_attribute("textContent")
                except:
                    print("Error with product: can't find the product. Link: ", request)
                    pass
                
                #If don't have the cash price the product is unavailable
                try:    
                    product_cash_price = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-5492faee-2.ipHrwP.finalPrice'))).get_attribute("textContent")
                except:
                    product_cash_price = ""
                
                #If don't have the card price the price is the same as the cash price
                try: 
                    product_card_price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'regularPrice'))).get_attribute("textContent")
                except:
                    product_card_price = product_cash_price
                    
                #If don't have the installments the product can't be purchased with cards
                try:    
                    product_card_installments= wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cardParcels'))).get_attribute("textContent")
                except:
                    product_card_installments = ""
                    
                #If the Code can't be found the site has been changed or the URL is incorrect      
                try:
                    driver.execute_script("window.scrollTo(0, 1000);")
                    #pattern = re.compile(r'- Modelo:\s*(.+?)\s*(Especificações|Recursos)', re.MULTILINE)
                    code = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.sc-7e0ca514-1.GiPKU'))).get_attribute("textContent")
                    pattern = re.compile(r'- Modelo:\s*(?:.*?PartNumber:\s*)?(.+?)\s*(Especificações|Recursos|Especificação|- Não)', re.MULTILINE)
                    result = pattern.search(code)
                    product_code = result.group(1)
                except Exception as e:
                    print("Error with product: can't find the product model. Link: " + request + " .Error: " + e )
                    pass
           

            #closes the driver connection and the page
            driver.quit()

            print(product_title)

            #Creates new rows with the today's price
            try:
                connection = ''  
                connection = self.db.get_connection()
                self.db.add(product_title, product_code, request, ecommerce, product_cash_price, product_card_price, product_card_installments, date_today, connection)
                self.db.commit(connection)
                self.db.quit(connection)
            except Exception as e:
                print("Erro ao inserir: ", e)
                sys.exit()

            
