import sqlite3
import pandas as pd
con = sqlite3.connect(".\src\database\shoppingitems.db")
cur = con.cursor()

prices_data = pd.read_csv("src\database\prices.csv", delimiter=',')
prices_data.to_sql('prices', con, index=False)

offer_data = pd.read_csv("src\database\offers.csv", delimiter=',')
offer_data.to_sql('offers', con, index=False)

print("Database Setup Complete")