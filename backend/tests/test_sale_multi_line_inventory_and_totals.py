from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multi_line_inventory_and_totals():
    # Create two products
    p1 = client.post("/products", json={"name":"ML1","sku":"ML-1","price":10.0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"ML2","sku":"ML-2","price":20.0,"gst_rate":12.0,"stock_qty":20}).json()

    start1 = p1["stock_qty"]
    start2 = p2["stock_qty"]

    r = client.post("/sales", json={
        "customer_name": "MultiLine",
        "line_items": [
            {"product_id": p1["id"], "qty": 3},
            {"product_id": p2["id"], "qty": 5}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    # Inventory decremented
    g1 = client.get(f"/products/{p1['id']}").json()
    g2 = client.get(f"/products/{p2['id']}").json()
    assert g1["stock_qty"] == start1 - 3
    assert g2["stock_qty"] == start2 - 5

    # Totals parseable
    Decimal(str(sale["subtotal"]))
    Decimal(str(sale["gst_total"]))
    Decimal(str(sale["grand_total"]))
