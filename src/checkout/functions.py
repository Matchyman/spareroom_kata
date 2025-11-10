from pydantic import BaseModel
from src.dao.daoRoutines import DaoRoutines

class CheckoutItem(BaseModel):
    code: str = ""
    quantity: int = 0

@staticmethod
async def calc_item_total(item: CheckoutItem) -> int:
    bob = await DaoRoutines().get_data()
    return item.quantity

@staticmethod
def check_item(item: CheckoutItem) -> int:
    return 250