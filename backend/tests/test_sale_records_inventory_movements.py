from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_records_inventory_movements():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 1:
        p = client.post("/products", json={"name":"ForMov","sku":"FM-1","price":5.0,"gst_rate":5.0,"stock_qty":10}).json()
        pid = p["id"]
    else:
        pid = products[0]["id"]

    before = client.get("/inventory/movements").json()

    sale = client.post("/sales", json={
        "customer_name": "MovRec",
        "line_items": [
            {"product_id": pid, "qty": 2}
        ]
    })
    assert sale.status_code in (200, 201), sale.text

    after = client.get("/inventory/movements").json()
    assert len(after) >= len(before) + 1
