from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_returns_linked_line_items_with_correct_fields():
    client.post("/seed")
    products = client.get("/products").json()
    assert len(products) >= 1
    p = products[0]
    pid = p["id"]

    resp = client.post("/sales", json={
        "customer_name": "LineLink",
        "line_items": [{"product_id": pid, "qty": 4}]
    })
    assert resp.status_code in (200, 201), resp.text
    sale = resp.json()
    assert isinstance(sale.get("line_items"), list) and sale["line_items"], "Line items missing"
    li = sale["line_items"][0]
    assert li["sale_id"] == sale["id"]
    assert li["product_id"] == pid
    assert int(li["qty"]) == 4
