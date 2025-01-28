import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

from database import database

class charts:
    
    db = None

    def __init__(self, db):
        self.db = db
        
    def update(self):
        #Gets a connection with the database and get all the products
        connection = self.db.get_connection()
        products = self.db.get_all(connection)
        
        
        products = self.transform_query_to_dict(products)
        list_of_known_products = {}
        
        
        for product in products:
            product_code = product["Code"]
            ecommerces =  product["Ecommerce"]
            if product_code not in list_of_known_products:
                list_of_known_products[product_code] = {
                    'products':  [],
                    'ecommerces': set()
                }
                
            list_of_known_products[product_code]["products"].append(product)
            list_of_known_products[product_code]["ecommerces"].add(ecommerces)
            
        #If it has two differents ecommerces in the list the plot is generated
        for known_products in list_of_known_products.values():
            if len(known_products["ecommerces"]) >= 2:
                self.generate(known_products['products'])


    #Generate the plot using Seaborn and MatPlotLib
    def generate(self, products):
        df = pd.DataFrame(products)
        #Some configs of the chart
        plt.figure(figsize=(14,7))
        plt.xticks(rotation=45)
        sns.set_theme(style="darkgrid")
        
        #Create the charte
        sns.lineplot(data=df, x="Date", y="Cash Price", hue="Ecommerce", marker="o", dashes=False, linewidth=2.5)
        
        #Labeling the chart
        plt.title("Price over days", fontsize=16, fontweight='bold')
        plt.xlabel("Date", fontsize=12, fontweight='bold')
        plt.ylabel("Cash Price", fontsize=12, fontweight='bold')
        plt.legend(title='Ecommerce', loc='upper left', bbox_to_anchor=(1,1))
        
        #More configs
        ax = plt.gca()
        ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=6))
        
        #Save the plot in a .png
        plt.tight_layout()
        product_name = self.clean_img_name(products[0]["Code"])
        plt.savefig("images/" + product_name + ".png", dpi=300)
        plt.close()
        
    #A function that transform a SQLite query to a list of dictionarys
    def transform_query_to_dict(self, products):
        list_of_dicts = [product for product in map(self.process_product, products) if product is not None]
        return list_of_dicts
    
    #Create the dictionary
    def process_product(self, product_item): 
        try:
            id, product, code, link, ecommerce, cash_price, card_price, installments, date = product_item
            return {
                'ID': id, 
                'Product': product, 
                'Code': code, 
                'Link': link, 
                'Ecommerce': ecommerce, 
                'Cash Price': float(cash_price.replace("R$", "").replace(".", "").replace(",", ".").strip()), 
                'Card Price': float(card_price.replace("R$", "").replace(".", "").replace(",", ".").strip()), 
                'Installmentes': installments, 
                'Date': date
            } 
        except:
            return None 
        
    #Clean the product code that contains invalid chars to name the png's    
    def clean_img_name(self, image_name):     
        invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in invalid_chars:
            image_name = image_name.replace(char, "")
            
        return image_name
        
        
