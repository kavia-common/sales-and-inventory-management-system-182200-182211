from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_number_accepts_special_chars_and_preserves():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "InvSpec", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_num = "INV/2025-αΩ-#001"
    inv_resp = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_num})
    assert inv_resp.status_code in (200, 201), inv_resp.text
    assert inv_resp.json()["invoice_number"] == inv_num
