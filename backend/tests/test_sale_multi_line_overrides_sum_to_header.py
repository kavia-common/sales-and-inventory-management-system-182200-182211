from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_multi_line_overrides_sum_to_header():
    # Create two products
    p1 = client.post("/products", json={"name": "Ovr1", "sku": "OVR-ML-1", "price": 10.0, "gst_rate": 5.0, "stock_qty": 20}).json()
    p2 = client.post("/products", json={"name": "Ovr2", "sku": "OVR-ML-2", "price": 20.0, "gst_rate": 12.0, "stock_qty": 20}).json()

    r = client.post("/sales", json={
        "customer_name": "MultiOvr",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "unit_price": 3.21, "gst_rate": 7.77},
            {"product_id": p2["id"], "qty": 3, "unit_price": 4.56, "gst_rate": 9.99}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    sub_sum = sum(Decimal(str(li["line_subtotal"])) for li in sale["line_items"])
    gst_sum = sum(Decimal(str(li["line_gst"])) for li in sale["line_items"])
    tot_sum = sum(Decimal(str(li["line_total"])) for li in sale["line_items"])

    assert Decimal(str(sale["subtotal"])) == sub_sum
    assert Decimal(str(sale["gst_total"])) == gst_sum
    assert Decimal(str(sale["grand_total"])) == tot_sum
