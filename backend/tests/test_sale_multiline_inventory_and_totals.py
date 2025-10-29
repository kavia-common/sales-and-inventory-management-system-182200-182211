from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multiline_inventory_and_totals():
    client.post("/seed")
    # ensure at least two products
    prods = client.get("/products").json()
    if len(prods) < 2:
        client.post("/products", json={"name": "Extra1", "sku": "EX1", "price": 7.5, "gst_rate": 5.0, "stock_qty": 50})
        client.post("/products", json={"name": "Extra2", "sku": "EX2", "price": 12.0, "gst_rate": 18.0, "stock_qty": 50})
        prods = client.get("/products").json()
    p1, p2 = prods[0], prods[1]

    # Capture initial stock
    p1_before = client.get(f"/products/{p1['id']}").json()["stock_qty"]
    p2_before = client.get(f"/products/{p2['id']}").json()["stock_qty"]

    sale_resp = client.post("/sales", json={
        "customer_name": "MultiLine",
        "line_items": [
            {"product_id": p1["id"], "qty": 2},
            {"product_id": p2["id"], "qty": 3}
        ]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale = sale_resp.json()

    # Validate totals are 2-decimal strings or numbers
    for k in ("subtotal", "gst_total", "grand_total"):
        Decimal(str(sale[k]))  # parseable

    # Validate stock decremented
    p1_after = client.get(f"/products/{p1['id']}").json()["stock_qty"]
    p2_after = client.get(f"/products/{p2['id']}").json()["stock_qty"]
    assert p1_after == int(p1_before) - 2
    assert p2_after == int(p2_before) - 3
