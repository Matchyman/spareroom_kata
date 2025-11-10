from pydantic import BaseModel
from src.dao.daoRoutines import DaoRoutines
from fastapi.logger import logger

class CheckoutItem(BaseModel):
    code: str = ""
    quantity: int = 0

#Orchestrator Function
async def get_total(item: CheckoutItem) -> int:
    item_data = await get_item_data(item_code=item.code.lower())
    if not item_data:
        logger.debug(f"No item data for {item}, returning 0")
        return 0
    print(item_data)
    item_total = calculate_total(item_data=item_data, quant=item.quantity)
    return item_total

async def get_item_data(item_code:str="") -> dict:
    if not item_code:
        return {}
    return await DaoRoutines().get_data_by_item(primary_key=item_code)

def calculate_total(item_data:dict, quant:int) -> int:
    offer_data = item_data.get("offer")
    if not offer_data:
        return item_data.get("price") * quant
    return calculate_total_with_offer (item_data=item_data, quant=quant)

def calculate_total_with_offer(item_data:dict, quant: int) -> int:
    offer_data = item_data.get("offer")
    total = 0
    while quant >= offer_data.get("amount"):
        total += offer_data.get("price")
        quant -= offer_data.get("amount")
    total += item_data.get("price") * quant
    return total