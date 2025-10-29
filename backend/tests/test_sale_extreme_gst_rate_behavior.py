from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_with_extreme_gst_rate_behavior():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    extreme_gst = 99.99
    resp = client.post("/sales", json={
        "customer_name": "ExtremeGST",
        "line_items": [{"product_id": pid, "qty": 1, "gst_rate": extreme_gst}]
    })
    # Accept either validation rejection or acceptance with high GST rate
    assert resp.status_code in (200, 201, 400, 422)
    if resp.status_code in (200, 201):
        sale = resp.json()
        li = sale["line_items"][0]
        # Ensure GST rate persisted as two-decimal value when accepted
        assert Decimal(str(li["gst_rate"])) == Decimal("99.99")
