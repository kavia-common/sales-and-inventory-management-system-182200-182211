from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_override_and_default_rounding_consistency():
    # Create two products
    p1 = client.post("/products", json={"name": "MixRound1", "sku": "MIX-RND-1", "price": 7.89, "gst_rate": 11.11, "stock_qty": 10}).json()
    p2 = client.post("/products", json={"name": "MixRound2", "sku": "MIX-RND-2", "price": 2.34, "gst_rate": 5.55, "stock_qty": 10}).json()

    # Override only the first line
    r = client.post("/sales", json={
        "customer_name": "MixedRound",
        "line_items": [
            {"product_id": p1["id"], "qty": 3, "unit_price": 1.005, "gst_rate": 7.505},
            {"product_id": p2["id"], "qty": 4}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()

    # Check rounding and header consistency
    sub_sum = sum(Decimal(str(li["line_subtotal"])) for li in sale["line_items"])
    gst_sum = sum(Decimal(str(li["line_gst"])) for li in sale["line_items"])
    tot_sum = sum(Decimal(str(li["line_total"])) for li in sale["line_items"])
    assert Decimal(str(sale["subtotal"])) == sub_sum
    assert Decimal(str(sale["gst_total"])) == gst_sum
    assert Decimal(str(sale["grand_total"])) == tot_sum

    for li in sale["line_items"]:
        # Ensure monetary fields quantized to 2 decimals
        for k in ("unit_price", "gst_rate", "line_subtotal", "line_gst", "line_total"):
            v = Decimal(str(li[k]))
            assert v == v.quantize(Decimal("0.01"))
