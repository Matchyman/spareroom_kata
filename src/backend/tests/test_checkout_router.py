from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock, AsyncMock
import pandas as pd
from main import app


def test_check_health():
    client = TestClient(app)
    r = client.get("/checkout/checkhealth")
    assert r.status_code == 200
    assert r.json() == {"message": "Checkout Route is working"}


@patch('src.backend.checkout.functions.ReadDao')
def test_checkout_post(mock_read_dao):
    """Test checkout POST with mocked ReadDao"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    mock_df = pd.DataFrame({
        'code': ['A'],
        'price': [50],
        'amount': [3],
        'offerprice': [140]
    })
    mock_dao_instance.get_item_and_offer = AsyncMock(return_value=mock_df)
    
    client = TestClient(app)
    payload = [{"code": "A", "quant": 1}]
    r = client.post("/checkout/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "Checkout complete"
    assert data["total"] == 50
    
@patch('src.backend.checkout.functions.ReadDao')
def test_prices_get(mock_read_dao):
    """Test prices GET with mocked ReadDao"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    return_value = [{
        "id": "1",
        "code": "B",
        "value": 40
    }]
    
    mock_dao_instance.get_all_items = AsyncMock(return_value= return_value)
    
    client = TestClient(app)
    r = client.get("/checkout/prices")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 4
    
@patch('src.backend.checkout.functions.ReadDao')
def test_prices_get(mock_read_dao):
    """Test prices GET with mocked ReadDao"""
    mock_dao_instance = MagicMock()
    mock_read_dao.return_value = mock_dao_instance
    
    return_value = [{
        "id": "1",
        "code": "B",
        "amount":3,
        "offerprice": 70
    }]
    
    mock_dao_instance.get_all_items = AsyncMock(return_value= return_value)
    
    client = TestClient(app)
    r = client.get("/checkout/offers")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 2
    
