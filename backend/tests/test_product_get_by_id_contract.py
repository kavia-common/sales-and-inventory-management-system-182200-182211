from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_product_get_by_id_contract():
    # Create a product
    resp = client.post("/products", json={
        "name": "Contract",
        "sku": "CON-TRACT-1",
        "price": 19.95,
        "gst_rate": 12.5,
        "stock_qty": 7
    })
    assert resp.status_code in (200, 201), resp.text
    pid = resp.json()["id"]

    # Fetch it back
    got = client.get(f"/products/{pid}")
    assert got.status_code == 200
    data = got.json()
    assert data["id"] == pid
    assert data["name"] == "Contract"
    assert data["sku"] == "CON-TRACT-1"
    # Ensure numeric fields are parseable
    Decimal(str(data["price"]))
    Decimal(str(data["gst_rate"]))
    assert isinstance(data["stock_qty"], int)
