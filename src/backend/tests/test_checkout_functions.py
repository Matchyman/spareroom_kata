import pytest
import pandas as pd
from unittest.mock import AsyncMock, patch, MagicMock
from src.backend.checkout.functions import get_item_data, CheckoutItem, get_total, calculate_total, calculate_total_with_offer


@pytest.mark.asyncio
async def test_get_item_data_empty():
    res = await get_item_data("")
    assert res == {}


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_item_data_existing(mock_read_dao):
    """Test get_item_data returns DataFrame with price"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    # Mock the async method
    mock_df = pd.DataFrame({
        'code': ['a'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    res = await get_item_data("a")
    
    assert isinstance(res, pd.DataFrame)
    assert res.iloc[0]['price'] == 50


@pytest.mark.asyncio
async def test_get_total_unknown():
    item = CheckoutItem(code="x", quant=1)
    total = await get_total(item)
    assert total == 0


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_total_known(mock_read_dao):
    """Test get_total with known item 'a'"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['a'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    item = CheckoutItem(code="a", quant=1)
    total = await get_total(item)
    assert total == 50


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_total_with_offer(mock_read_dao):
    """Test item 'a' with quantity for special offer (3 items)"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['a'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    item = CheckoutItem(code="a", quant=3)
    total = await get_total(item)
    assert total == 140


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_total_with_offer_and_remainder(mock_read_dao):
    """Test item 'a' with quantity more than offer (4 items = 1 offer + 1 regular)"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['a'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    item = CheckoutItem(code="a", quant=4)
    total = await get_total(item)
    assert total == 190  # 140 for 3 items + 50 for 1 item


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_total_with_multiple_offers(mock_read_dao):
    """Test item 'a' with quantity for multiple offers (6 items = 2 offers)"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['a'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    item = CheckoutItem(code="a", quant=6)
    total = await get_total(item)
    assert total == 280  # 140 + 140


@pytest.mark.asyncio
@patch('src.backend.checkout.functions.ReadDao')
async def test_get_total_item_without_offer(mock_read_dao):
    """Test item 'c' which has no special offer"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['c'],
        'price': [25],
        'amount': [None],
        'offerprice': [None]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    item = CheckoutItem(code="c", quant=3)
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
    item_data = pd.DataFrame({
        'price': [25],
        'amount': [None],
        'offerprice': [None]
    })
    total = calculate_total(item_data=item_data, quant=2)
    assert total == 50


def test_calculate_total_with_offer_exact():
    """Test calculate_total_with_offer function with exact offer quantity"""
    item_data = pd.DataFrame({
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    total = calculate_total_with_offer(item_data=item_data, quant=3)
    assert total == 140


def test_calculate_total_with_offer_multiple():
    """Test calculate_total_with_offer function with multiple offer quantities"""
    item_data = pd.DataFrame({
        'price': [35],
        'amount': [2],
        'offerprice': [60]
    })
    total = calculate_total_with_offer(item_data=item_data, quant=5)
    assert total == 155  # (60 * 2) + (35 * 1) - two offers plus one regular price

