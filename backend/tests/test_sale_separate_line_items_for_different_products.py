from decimal import Decimal
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_separate_line_items_for_different_products():
    p1 = client.post("/products", json={"name":"Sep1","sku":"SEP-1","price":5.0,"gst_rate":5.0,"stock_qty":10}).json()
    p2 = client.post("/products", json={"name":"Sep2","sku":"SEP-2","price":7.0,"gst_rate":12.0,"stock_qty":10}).json()

    r = client.post("/sales", json={
        "customer_name": "SeparateLines",
        "line_items": [
            {"product_id": p1["id"], "qty": 1},
            {"product_id": p2["id"], "qty": 2}
        ]
    })
    assert r.status_code in (200, 201), r.text
    sale = r.json()
    assert isinstance(sale["line_items"], list) and len(sale["line_items"]) == 2
    # Subtotal 5 + 14 = 19; GST 0.25 + 1.68 = 1.93; Total 20.93
    assert str(Decimal(str(sale["subtotal"]))) == str(Decimal("19.00"))
    assert str(Decimal(str(sale["gst_total"]))) == str(Decimal("1.93"))
    assert str(Decimal(str(sale["grand_total"]))) == str(Decimal("20.93"))
