from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_list_keys_consistency():
    client.post("/seed")
    r = client.get("/products")
    assert r.status_code == 200
    lst = r.json()
    assert isinstance(lst, list)
    if lst:
        keys = set(lst[0].keys())
        assert {"id", "name", "sku", "price", "gst_rate", "stock_qty"} <= keys

def test_invoices_list_keys_consistency():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "SchemaKeys", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_number = f"INV-SCHEMA-{sale['id']}"
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_number})

    r = client.get("/invoices")
    assert r.status_code == 200
    lst = r.json()
    assert isinstance(lst, list)
    if lst:
        keys = set(lst[0].keys())
        assert {"id", "sale_id", "invoice_number", "date", "subtotal", "gst_total", "grand_total"} <= keys
