from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_invoices_list_after_multiple_creations():
    client.post("/seed")
    products = client.get("/products").json()
    if not products:
        return
    pid = products[0]["id"]

    s1 = client.post("/sales", json={"customer_name": "InvMulti1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    s2 = client.post("/sales", json={"customer_name": "InvMulti2", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    client.post("/invoices", json={"sale_id": s1["id"], "invoice_number": f"INV-MULTI-{s1['id']}"})
    client.post("/invoices", json={"sale_id": s2["id"], "invoice_number": f"INV-MULTI-{s2['id']}"})

    r = client.get("/invoices")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
    assert len(r.json()) >= 2
