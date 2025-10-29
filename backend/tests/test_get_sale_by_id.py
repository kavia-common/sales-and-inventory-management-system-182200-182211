from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_sale_by_id():
    # Seed and create sale
    client.post("/seed")
    sale_resp = client.post("/sales", json={
        "customer_name": "Get Sale",
        "line_items": [{"product_id": 1, "qty": 1}]
    })
    assert sale_resp.status_code in (200, 201), sale_resp.text
    sale_id = sale_resp.json()["id"]

    # Fetch by id
    get_resp = client.get(f"/sales/{sale_id}")
    assert get_resp.status_code == 200
    sale = get_resp.json()
    assert sale["id"] == sale_id
    assert "line_items" in sale and isinstance(sale["line_items"], list)
