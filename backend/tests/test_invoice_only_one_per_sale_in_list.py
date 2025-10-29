from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoice_list_contains_single_entry_per_sale():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "SingleInvPerSale", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    inv_no = f"INV-ONE-{sale['id']}"
    r1 = client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no})
    assert r1.status_code in (200, 201), r1.text
    # Attempt second invoice should fail as covered elsewhere; still verify list has exactly one
    client.post("/invoices", json={"sale_id": sale["id"], "invoice_number": inv_no + "-X"})
    lst = client.get("/invoices", params={"sale_id": sale["id"]})
    assert lst.status_code == 200
    items = [i for i in lst.json() if i.get("sale_id") == sale["id"]]
    assert len(items) == 1
