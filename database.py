import sqlite3


class database:
    con = ''
    cursor = ''
    def __init__(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            product VARCHAR(255) NOT NULL,
            link VARCHAR(255) NOT NULL,
            ecommerce VARCHAR(255) NOT NULL,
            cashprice VARCHAR(255),
            cardprice VARCHAR(255),
            installments VARCHAR(255),
            date VARCHAR(255) NOT NULL
            )""")
        self.con.commit()
    
    #CRUD
    def add(self, product, link, ecommerce, cash_price, card_price, installments, date):
        try:
            insert = (product, link, ecommerce, cash_price, card_price, installments, date)
            self.cursor.execute("""INSERT INTO products(product, link, ecommerce, cashprice, cardprice, installments, date) 
                                VALUES(?,?,?,?,?,?,?)""", insert)
        except Exception as e:
            print("Insertion error: ", e)
            
            
    def read(self, id):
        try:
            result = self.cursor.execute('SELECT * FROM products WHERE id=?', id)
            return result.fetchone()
            
        except Exception as e:
            print("Read error: ", e)
            
    def update(self, id, product, link, ecommerce, cash_price, card_price, installments, date):
        try:
            update = (product, link, ecommerce, product, link, ecommerce, cash_price, card_price, installments, date, id)
            self.cursor.execute("""UPDATE products SET product=?, link=?, ecommerce=?, cashprice=?, cardprice=?, installments=?, date=?
                                WHERE id=?""", update)
        except Exception as e:
            print("Update error: ", e)
            
    def  delete(self, id):
        try:
            self.cursor.execute('DELETE FROM products WHERE id=?',id)
        except Exception as e:
            print("delete error: ", e)
            
            
    #Help functions
    def get_id_by_product(self, product):
        try:
            result = self.cursor.execute('SELECT id FROM products WHERE product=?', product)
            return result.fetchone()
        except Exception as e:
            print("Get id error: ", e)
                
    def commit(self):
        self.con.commit()
            
    def get_connection(self):
        return self.con
            
    def quit(self):
        self.get_connection().close
            

