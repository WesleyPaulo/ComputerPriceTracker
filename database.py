

import sqlite3


class database:
    def __init__(self):
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            product VARCHAR(255) NOT NULL,
            link VARCHAR(255) NOT NULL,
            ecommerce VARCHAR(255) NOT NULL,
            cashprice VARCHAR(255),
            cardprice VARCHAR(255),
            installments VARCHAR(255),
            date VARCHAR(255) NOT NULL
            )""")
        con.commit()
        con.close()
    
    #CRUD
    def add(self, product, link, ecommerce, cash_price, card_price, installments, date, connection):
        try:
            cursor = connection.cursor()
            insert = (product, link, ecommerce, cash_price, card_price, installments, date)
            cursor.execute("""INSERT INTO products(product, link, ecommerce, cashprice, cardprice, installments, date) 
                                VALUES(?,?,?,?,?,?,?)""", insert)
        except Exception as e:
            print("Insertion error: ", e)
            
            
    def read(self, id, connection):
        try:
            cursor = connection.cursor()
            result = cursor.execute('SELECT * FROM products WHERE id=?', id)
            return result.fetchone()
            
        except Exception as e:
            print("Read error: ", e)
            
    def update(self, id, product, link, ecommerce, cash_price, card_price, installments, date, connection):
        try:
            cursor = connection.cursor()
            update = (product, link, ecommerce, product, link, ecommerce, cash_price, card_price, installments, date, id)
            cursor.execute("""UPDATE products SET product=?, link=?, ecommerce=?, cashprice=?, cardprice=?, installments=?, date=?
                                WHERE id=?""", update)
        except Exception as e:
            print("Update error: ", e)
            
    def  delete(self, id, connection):
        try:
            cursor = connection.cursor()
            cursor.execute('DELETE FROM products WHERE id=?',id)
        except Exception as e:
            print("delete error: ", e)
            
            
    #Help functions
    def get_id_by_product(self, product, connection):
        try:
            cursor = connection.cursor()
            result = cursor.execute('SELECT id FROM products WHERE product=?', product)
            return result.fetchone()
        except Exception as e:
            print("Get id error: ", e)
                
    def commit(self, connection):
        connection.commit()
            
    def get_connection(self):
        return sqlite3.connect("database.db")
            
    def quit(self, connection):
        connection.close()
            

