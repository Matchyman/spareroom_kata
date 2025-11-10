from fastapi.testclient import TestClient
from main import app


def test_root():
    client = TestClient(app)
    r = client.get("/")
    assert r.status_code == 200
    assert r.json() == {"message": "API is running"}



