from src.backend.database.dbConnectionFactory import DBConnectionFactory
import json
import pandas as pd


class ReadDao:
    def __init__(self):
        self.dao = DBConnectionFactory()
    
    
    async def get_all_items(self, table:str):
        connection = self.dao.connect()
        query = f"SELECT * from {table}"
        data = self.dao.get_data(con=connection, query=query, table = table)
        self.dao.close_connection(con=connection)
        return json.loads(data.to_json(orient="records"))
    
    async def get_single_item(self, table:str, column:str, value:str):
        connection = self.dao.connect()
        query = f"SELECT * from {table} WHERE {column} = '{value}'"
        data = self.dao.get_data(con=connection, query=query, table=table)
        self.dao.close_connection(con =connection)
        return json.loads(data.to_json(orient="records"))
    
    async def get_item_and_offer(self, table:str, column:str, value:str):
        connection = self.dao.connect()
        query = f"""SELECT prices.code, prices.price, offers.amount, offers.offerprice 
                    FROM {table} 
                    LEFT JOIN offers 
                    ON prices.code = offers.code
                    WHERE {table}.{column} = '{value}'"""
        
        data = self.dao.get_data(con=connection, query=query, table = table)
        self.dao.close_connection(con = connection)
        return data
    
    
def main():
    bob = ReadDao().get_single_item(table="prices", column="id", value="1")
    print(bob)
    
if __name__ == "__main__":
    main()