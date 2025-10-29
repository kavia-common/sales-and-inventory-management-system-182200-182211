from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_product_update_numeric_fields_persistence():
    p = client.post("/products", json={
        "name": "NumPersist",
        "sku": "NUM-PER-1",
        "price": 9.50,
        "gst_rate": 5.00,
        "stock_qty": 3
    }).json()
    r = client.put(f"/products/{p['id']}", json={"price": 10.75, "gst_rate": 12.5, "stock_qty": 8})
    assert r.status_code == 200, r.text
    updated = r.json()
    assert str(Decimal(str(updated["price"]))) == str(Decimal("10.75"))
    assert str(Decimal(str(updated["gst_rate"]))) == str(Decimal("12.50"))
    assert int(updated["stock_qty"]) == 8
