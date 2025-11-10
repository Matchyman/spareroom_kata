import asyncio
from src.dao.daoRoutines import DaoRoutines

async def main():
    # Create an instance of DaoRoutines
    dao = DaoRoutines()
    
    # Get all pricing data
    all_data = await dao.get_data()
    print("All pricing data:", all_data)
    
    # Get pricing for a specific item (e.g., 'a')
    item_a = await dao.get_data_by_item('a')
    print("\nPricing for item A:", item_a)

# Run the async main function
asyncio.run(main())