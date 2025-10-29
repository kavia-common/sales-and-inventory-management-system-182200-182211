from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movement_reason_unicode():
    r = client.post("/products", json={
        "name": "UnicodeReason",
        "sku": "UNIC-REASON-1",
        "price": 1.0,
        "gst_rate": 0.0,
        "stock_qty": 0
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    reason = "Restock – batch №42 • 特殊字符 ✅"
    mv = client.post("/inventory/movements", json={"product_id": pid, "change_qty": 5, "reason": reason})
    assert mv.status_code in (200, 201), mv.text
    assert mv.json()["reason"] == reason
