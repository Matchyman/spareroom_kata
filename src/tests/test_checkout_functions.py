import pytest
from src.checkout.functions import get_item_data, CheckoutItem, get_total, calculate_total, calculate_total_with_offer


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


@pytest.mark.asyncio
async def test_get_total_with_offer():
    """Test item 'a' with quantity for special offer (3 items)"""
    item = CheckoutItem(code="a", quantity=3)
    total = await get_total(item)
    assert total == 140


@pytest.mark.asyncio
async def test_get_total_with_offer_and_remainder():
    """Test item 'a' with quantity more than offer (4 items = 1 offer + 1 regular)"""
    item = CheckoutItem(code="a", quantity=4)
    total = await get_total(item)
    assert total == 190  # 140 for 3 items + 50 for 1 item


@pytest.mark.asyncio
async def test_get_total_with_multiple_offers():
    """Test item 'a' with quantity for multiple offers (6 items = 2 offers)"""
    item = CheckoutItem(code="a", quantity=6)
    total = await get_total(item)
    assert total == 280  # 140 + 140


@pytest.mark.asyncio
async def test_get_total_item_without_offer():
    """Test item 'c' which has no special offer"""
    item = CheckoutItem(code="c", quantity=3)
    total = await get_total(item)
    assert total == 75  # 25 * 3


@pytest.mark.asyncio
async def test_get_total_zero_quantity():
    """Test with zero quantity"""
    item = CheckoutItem(code="a", quantity=0)
    total = await get_total(item)
    assert total == 0


def test_calculate_total_no_offer():
    """Test calculate_total function with item having no offer"""
    item_data = {"price": 25}
    total = calculate_total(item_data=item_data, quant=2)
    assert total == 50


def test_calculate_total_with_offer_exact():
    """Test calculate_total_with_offer function with exact offer quantity"""
    item_data = {
        "price": 50,
        "offer": {
            "amount": 3,
            "price": 140
        }
    }
    total = calculate_total_with_offer(item_data=item_data, quant=3)
    assert total == 140


def test_calculate_total_with_offer_multiple():
    """Test calculate_total_with_offer function with multiple offer quantities"""
    item_data = {
        "price": 35,
        "offer": {
            "amount": 2,
            "price": 60
        }
    }
    total = calculate_total_with_offer(item_data=item_data, quant=5)
    assert total == 155  # (60 * 2) + (35 * 1) - two offers plus one regular price
