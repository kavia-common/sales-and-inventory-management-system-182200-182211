from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_update_multiple_fields_on_product():
    # Create a product
    r = client.post("/products", json={
        "name": "MultiBefore",
        "sku": "MULTI-1",
        "price": 1.23,
        "gst_rate": 5.5,
        "stock_qty": 2
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # Update several fields at once
    upd = client.put(f"/products/{pid}", json={
        "name": "MultiAfter",
        "price": 9.87,
        "gst_rate": 18.0,
        "stock_qty": 12
    })
    assert upd.status_code == 200, upd.text
    data = upd.json()
    assert data["name"] == "MultiAfter"
    assert Decimal(str(data["price"])) == Decimal("9.87")
    assert Decimal(str(data["gst_rate"])) == Decimal("18.0")
    assert data["stock_qty"] == 12
