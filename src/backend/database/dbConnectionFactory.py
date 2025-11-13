import sqlite3
import yaml
import logging
import pandas as pd
from yaml.loader import SafeLoader

class DBConnectionFactory:
    
    def __init__(self):
        self.config = {}
        with open("./config/config.yml", "r") as file:
            self.config = yaml.load(file, Loader=SafeLoader)
        self.logger = logging.getLogger()
        self.dbpath = self.config.get("dbpath")
            
    def connect(self) -> sqlite3.Connection:
        try:
            con = sqlite3.connect(self.dbpath)
            return con
        except sqlite3.OperationalError as ce:
            self.logger.warning(f"WARNING: No connection made with DB: {self.dbpath}, Error: {ce}")
        except Exception as e:
            self.logger.error(f"ERROR: {e} in dbConnectionFactory - connect function")
            
    def add_data(self, con: sqlite3.Connection, query: str, table:str):
        if self.check_table(con=con, table=table):
            cur = con.cursor()
            try:
                cur.execute(query)
                con.commit()
            except sqlite3.DatabaseError as dberr:
                raise sqlite3.DatabaseError(dberr)
        else:
            raise sqlite3.DatabaseError(f"No table found for : {table}")
            
           
    def check_table(self, con: sqlite3.Connection, table:str):
        cur = con.cursor()
        res = cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{table}'")
        if res.fetchall() == []:
            return False
        return True

    def get_data(self, con:sqlite3.Connection, query:str, table:str):
        if not self.check_table(con=con, table=table):
            raise sqlite3.DatabaseError(f"No table found for : {table}")
        return pd.read_sql(sql=query, con=con)
    
    def close_connection(self, con:sqlite3.Connection):
        con.close()


    