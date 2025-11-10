from fastapi import APIRouter
from fastapi.logger import logger
from src.checkout.functions import CheckoutItem, get_total

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
        logger.info(f"Code: {item.code}, Quant:{item.quantity}")
    return {"message": "Checkout complete", "total": subtotal}