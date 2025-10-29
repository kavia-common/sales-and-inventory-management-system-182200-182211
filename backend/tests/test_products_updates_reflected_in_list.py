from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_products_updates_are_reflected_in_list():
    # Create product
    r = client.post("/products", json={
        "name": "Updatable",
        "sku": "UPD-1",
        "price": 4.56,
        "gst_rate": 5.0,
        "stock_qty": 3
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    # First update
    u1 = client.put(f"/products/{pid}", json={"name": "Updatable-1", "price": 7.89})
    assert u1.status_code == 200, u1.text

    # Second update
    u2 = client.put(f"/products/{pid}", json={"gst_rate": 12.0, "stock_qty": 10})
    assert u2.status_code == 200, u2.text

    # Verify via list
    lst = client.get("/products")
    assert lst.status_code == 200
    items = lst.json()
    found = next((p for p in items if p["id"] == pid), None)
    assert found is not None
    assert found["name"] == "Updatable-1"
    assert Decimal(str(found["price"])) == Decimal("7.89")
    assert Decimal(str(found["gst_rate"])) == Decimal("12.0")
    assert found["stock_qty"] == 10
