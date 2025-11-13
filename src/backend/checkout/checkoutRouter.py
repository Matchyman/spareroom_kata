from fastapi import APIRouter
from fastapi.logger import logger
from src.backend.dao.readDao import ReadDao
from src.backend.checkout.functions import CheckoutItem, get_total


router = APIRouter(
    prefix = "/checkout",
    tags=["checkout"]
)

@router.get("/checkhealth")
def check_route() -> dict:
    """
    Checks that route is working correctly
    
    Returns:
        dict: Information confirming health
    """
    return {"message": "Checkout Route is working"}

@router.get("/prices")
async def get_prices() -> list[dict]:
    "Gets all prices from prices table"
    price_data = await ReadDao().get_all_items(table="prices")
    return price_data

@router.get("/prices/{priceid}")
async def get_price_with_id(priceid:int) -> list[dict]:
    """
    Get single offer from offer table
    
    Input:
        priceid: int -> id offer you want to retrieve
        
    Returns:
        item: list[dict] -> the item
    """
    price_data = await ReadDao().get_single_item(table="prices", column="id", value=str(priceid))
    return price_data

@router.get("/offers")
async def get_offers() -> list[dict]:
    "Gets all offers from offers table"
    offer_data = await ReadDao().get_all_items(table="offers")
    return offer_data

@router.get("/offer/{offerid}")
async def get_offer_with_id(offerid:int) -> list[dict]:
    """
    Get single offer from offer table
    
    Input:
        offerid: int -> id offer you want to retrieve
        
    Returns:
        offer: list[dict] -> the offer
    """
    offer_data = await ReadDao().get_single_item(table="offers", column="id", value=str(offerid))
    return offer_data

@router.post("/")
async def checkout(items:list[CheckoutItem]) -> dict:
    """
    Takes checkout list and returns a subtotal
    
    Input:
        items: List of items
        
    Returns:
        int: subtotal of items
    """
    subtotal = 0
    for item in items:
        subtotal += await get_total(item)
        logger.info(f"Code: {item.code}, Quant:{item.quant}")
    return {"message": "Checkout complete", "total": subtotal}