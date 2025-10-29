from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_filters_by_number_and_sale_id():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    # Create sale and invoice
    sale = client.post("/sales", json={"customer_name": "FilterTest", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = f"INV-FILTER-{sale['id']}"
    inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv.status_code in (200, 201), inv.text

    # Filter by invoice_number
    by_num = client.get("/invoices", params={"invoice_number": inv_num})
    assert by_num.status_code == 200
    lst = by_num.json()
    assert lst and lst[0]["invoice_number"] == inv_num

    # Filter by sale_id
    by_sale = client.get("/invoices", params={"sale_id": sale["id"]})
    assert by_sale.status_code == 200
    lst2 = by_sale.json()
    assert lst2 and lst2[0]["sale_id"] == sale["id"]
