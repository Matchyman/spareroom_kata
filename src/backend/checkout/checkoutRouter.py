from fastapi import APIRouter
from fastapi.logger import logger
from src.backend.checkout.functions import CheckoutItem, get_total, get_all_prices

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
    return await get_all_prices()

@router.get("/offers")
async def get_offers() -> list[dict]:
    return await get_all_offers()

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