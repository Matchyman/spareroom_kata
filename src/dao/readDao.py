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