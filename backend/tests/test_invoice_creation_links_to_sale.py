from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_creation_links_to_sale():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "LinkCheck", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-LINK-{sale['id']}"
    r_inv = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r_inv.status_code in (200, 201), r_inv.text
    inv = r_inv.json()
    assert inv["sale_id"] == sale["id"]
    assert inv["invoice_number"] == inv_no
