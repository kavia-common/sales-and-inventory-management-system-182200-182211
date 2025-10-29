from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_for_same_sale_rejected_with_400():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale = client.post("/sales", json={"customer_name": "DupSaleInv", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-DUPSALE-{sale['id']}"})
    assert inv1.status_code in (200, 201), inv1.text

    inv2 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": f"INV-DUPSALE-{sale['id']}-2"})
    assert inv2.status_code == 400
    assert "already exists for this sale" in inv2.json().get("detail", "")
