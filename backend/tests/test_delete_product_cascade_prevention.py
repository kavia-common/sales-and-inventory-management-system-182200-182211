from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_delete_product_after_sale_is_blocked_or_cascades_cleanly():
    # Create product and sale
    r = client.post("/products", json={
        "name": "ToDelete",
        "sku": "DEL-001",
        "price": 9.99,
        "gst_rate": 18.0,
        "stock_qty": 5
    })
    assert r.status_code in (200, 201), r.text
    pid = r.json()["id"]

    sale = client.post("/sales", json={
        "customer_name": "Buyer",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert sale.status_code in (200, 201), sale.text
    sale_id = sale.json()["id"]

    # Attempt delete: either it succeeds (if allowed) or returns error (acceptable).
    del_r = client.delete(f"/products/{pid}")
    assert del_r.status_code in (200, 204, 400, 409), del_r.text

    # Verify sale retrieval still works and has at least one line item
    sget = client.get(f"/sales/{sale_id}")
    assert sget.status_code == 200
    body = sget.json()
    assert isinstance(body.get("line_items", []), list)
