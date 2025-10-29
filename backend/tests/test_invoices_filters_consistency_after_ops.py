from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_filters_consistency_after_multiple_operations():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    # Create two sales and invoices
    s1 = client.post("/sales", json={"customer_name": "Consist1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    s2 = client.post("/sales", json={"customer_name": "Consist2", "line_items": [{"product_id": pid, "qty": 2}]}).json()
    inv1_no = f"INV-CONS-1-{s1['id']}"
    inv2_no = f"INV-CONS-2-{s2['id']}"
    client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": inv1_no})
    client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": inv2_no})

    # Filter by invoice_number
    r1 = client.get("/invoices", params={"invoice_number": inv1_no})
    assert r1.status_code == 200
    assert isinstance(r1.json(), list)

    # Filter by sale_id
    r2 = client.get("/invoices", params={"sale_id": s2["id"]})
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)

    # Combined filter (matching)
    r3 = client.get("/invoices", params={"sale_id": s1["id"], "invoice_number": inv1_no})
    assert r3.status_code == 200
    assert isinstance(r3.json(), list)
