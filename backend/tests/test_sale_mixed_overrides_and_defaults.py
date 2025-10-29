from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_mixed_overrides_and_defaults():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 2:
        return
    p1, p2 = products[0], products[1]
    # Only override for first line item
    r = client.post("/sales", json={
        "customer_name": "Mixed",
        "line_items": [
            {"product_id": p1["id"], "qty": 2, "unit_price": 4.44, "gst_rate": 6.66},
            {"product_id": p2["id"], "qty": 3}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert len(sale["line_items"]) == 2
    li1 = next(li for li in sale["line_items"] if li["product_id"] == p1["id"])
    li2 = next(li for li in sale["line_items"] if li["product_id"] == p2["id"])

    # Overrides persisted for first item
    assert str(li1["unit_price"]).startswith("4.44")
    assert str(li1["gst_rate"]).startswith("6.66")

    # Defaults used for second item
    assert str(li2["unit_price"]).startswith(str(Decimal(str(p2["price"])).quantize(Decimal("0.01"))))
    assert str(li2["gst_rate"]).startswith(str(Decimal(str(p2["gst_rate"])).quantize(Decimal("0.01"))))
