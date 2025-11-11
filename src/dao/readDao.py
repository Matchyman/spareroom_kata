from src.database.dbConnectionFactory import DBConnectionFactory


class ReadDao:
    def __init__(self):
        self.dao = DBConnectionFactory()
    
    
    async def get_all_items(self, table:str):
        connection = self.dao.connect()
        query = f"SELECT * from {table}"
        data = self.dao.get_data(con=connection, query=query)
        self.dao.close_connection()
        return data
    
    async def get_single_item(self, table:str, column:str, value:str):
        connection = self.dao.connect()
        query = f"SELECT * from {table} WHERE {column} = '{value}'"
        data = self.dao.get_data(con=connection, query=query)
        self.dao.close_connection()
        return data
    
    def get_item_and_offer(self, table:str, column:str, value:str):
        connection = self.dao.connect()
        query = f"""SELECT prices.code, prices.price, offers.amount, offers.offerprice 
                    FROM {table} 
                    LEFT JOIN offers 
                    ON prices.code = offers.code
                    WHERE {table}.{column} = '{value}'"""
        data = self.dao.get_data(con=connection, query=query)
        self.dao.close_connection()
        return data
    
    
def main():
    ReadDao().get_item_and_offer(table='prices', column="code", value="A")
    
if __name__ == "__main__":
    main()
