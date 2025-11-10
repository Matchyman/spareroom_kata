from fastapi import APIRouter


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
def checkout(items:list[dict]):
    subtotal = 0
    for item in items:
        break
        
    return {"message": "Checkout complete"}