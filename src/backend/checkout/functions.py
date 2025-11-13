from pydantic import BaseModel
from src.backend.dao.readDao import ReadDao
from fastapi.logger import logger

class CheckoutItem(BaseModel):
    code: str = ""
    quant: int = 0
    
#Orchestrator Function
async def get_total(item: CheckoutItem) -> int:
    item_data = await get_item_data(item_code=item.code)
    if item_data.empty:
        logger.debug(f"No item data for {item}, returning 0")
        return 0
    item_total = calculate_total(item_data=item_data, quant=item.quant)
    return item_total

async def get_item_data(item_code:str="") -> dict:
    if not item_code:
        return {}
    return await ReadDao().get_item_and_offer(table ="prices", column="code", value=item_code)

def calculate_total(item_data, quant:int) -> int:
    offer_amount = item_data["amount"].item()
    offer_value = item_data["offerprice"].item()
    if not offer_amount and not offer_value:
        return item_data["price"].item() * quant
    return calculate_total_with_offer (item_data=item_data, quant=quant)

def calculate_total_with_offer(item_data:dict, quant: int) -> int:
    offer_amount = item_data["amount"].item()
    offer_value = item_data["offerprice"].item()
    total = 0
    while quant >= offer_amount:
        total += offer_value
        quant -= offer_amount
    total += item_data["price"].item() * quant
    return total

