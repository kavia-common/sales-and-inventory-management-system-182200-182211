from fastapi.testclient import TestClient
from src.api.main import app

def test_sale_no_line_items_returns_400():
    client = TestClient(app)
    resp = client.post("/sales", json={"customer_name": "No Items", "line_items": []})
    assert resp.status_code == 400
    assert "No line items provided" in resp.text
