import json
import asyncio


class DaoRoutines:
    
    def __init__(self):
        with open("src\\backend\\dao\\pricing.json", "r") as f:
            self.data = json.load(f)
    
    async def get_data(self):
        # Long function
        await asyncio.sleep(1)
        return self.data

    async def get_data_by_item(self, primary_key):
        # Quick function
        await asyncio.sleep(0.05)
        return self.data.get(primary_key)
