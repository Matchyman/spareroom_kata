import pytest
from src.checkout.functions import get_item_data, CheckoutItem, get_total


@pytest.mark.asyncio
async def test_get_item_data_empty():
    res = await get_item_data("")
    assert res == {}


@pytest.mark.asyncio
async def test_get_item_data_existing():
    res = await get_item_data("a")
    assert isinstance(res, dict)
    assert res.get("price") == 50


@pytest.mark.asyncio
async def test_get_total_unknown():
    item = CheckoutItem(code="x", quantity=1)
    total = await get_total(item)
    assert total == 0


@pytest.mark.asyncio
async def test_get_total_known():
    item = CheckoutItem(code="a", quantity=1)
    total = await get_total(item)
    assert total == 50
