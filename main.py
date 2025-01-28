
from updater import updater
from database import database
from charts import charts
#from database_creator import database_creator

def main():

    #Initialize database and paths
    db = database()
    data_path = "data.txt"
    driver_path = "chromedriver.exe"

    #Update the dataset with the today data
    updt = updater(driver_path, data_path, db)
    updt.update()
    
    #Create/Update the charts of the data set after the database update
    ct = charts(db)
    ct.update()

if __name__ == "__main__":
    main()