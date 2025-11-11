import sqlite3
con = sqlite3.connect(".\src\database\shoppingitems.db")
cur = con.cursor()
cur.execute("""CREATE TABLE prices(
    code str UNIQUE, 
    price int
    )""")
cur.execute("""CREATE TABLE offers(
    code str UNIQUE, 
    offeramount int, 
    offerprice int
    )""")
