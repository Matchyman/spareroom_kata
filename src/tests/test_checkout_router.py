from fastapi.testclient import TestClient
from main import app


def test_check_health():
    client = TestClient(app)
    r = client.get("/checkout/checkhealth")
    assert r.status_code == 200
    assert r.json() == {"message": "Checkout Route is working"}


def test_checkout_post():
    client = TestClient(app)
    payload = [{"code": "a", "quantity": 1}]
    r = client.post("/checkout/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["message"] == "Checkout complete"
    assert data["total"] == 50
