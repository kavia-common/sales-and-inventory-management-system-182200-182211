from fastapi.testclient import TestClient
from decimal import Decimal
from src.api.main import app

client = TestClient(app)

def test_update_preserves_unspecified_fields():
    # Create initial product
    r = client.post("/products", json={
        "name": "PreserveOld",
        "sku": "PRES-1",
        "price": 20.50,
        "gst_rate": 18.0,
        "stock_qty": 9
    })
    assert r.status_code in (200, 201), r.text
    p = r.json()
    pid = p["id"]

    # Update only the name
    upd = client.put(f"/products/{pid}", json={"name": "PreserveNew"})
    assert upd.status_code == 200, upd.text
    data = upd.json()
    assert data["name"] == "PreserveNew"
    # Unspecified fields remain unchanged
    assert data["sku"] == "PRES-1"
    assert Decimal(str(data["price"])) == Decimal("20.50")
    assert Decimal(str(data["gst_rate"])) == Decimal("18.0")
    assert data["stock_qty"] == 9
