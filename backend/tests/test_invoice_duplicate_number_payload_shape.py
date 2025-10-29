from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_duplicate_invoice_number_payload_shape():
    client.post("/seed")
    products = client.get("/products").json()
    assert products
    pid = products[0]["id"]

    sale1 = client.post("/sales", json={"customer_name": "Shape1", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    sale2 = client.post("/sales", json={"customer_name": "Shape2", "line_items": [{"product_id": pid, "qty": 1}]}).json()

    inv_no = "INV-SHAPE-001"
    ok = client.post("/invoices", json={"sale_id": sale1["id"], "invoice_number": inv_no})
    assert ok.status_code in (200, 201), ok.text

    dup = client.post("/invoices", json={"sale_id": sale2["id"], "invoice_number": inv_no})
    assert dup.status_code == 400
    data = dup.json()
    assert isinstance(data, dict)
    assert "detail" in data
    assert isinstance(data["detail"], str)
