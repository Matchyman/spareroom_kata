import sqlite3
import pandas as pd
con = sqlite3.connect("./src/backend/database/shoppingitems.db")
cur = con.cursor()

prices_data = pd.read_csv("./src/backend/database/prices.csv", delimiter=',')
prices_data.to_sql('prices', con, index=False, if_exists="append")

offer_data = pd.read_csv("./src/backend/database/offers.csv", delimiter=',')
offer_data.to_sql('offers', con, index=False, if_exists="append")

print("Database Setup Complete")