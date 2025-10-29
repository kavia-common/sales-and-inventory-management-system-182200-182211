from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_get_sale_by_id_returns_200_and_payload():
    client.post("/seed")
    # Create a sale
    products = client.get("/products").json()
    pid = products[0]["id"]
    created = client.post("/sales", json={
        "customer_name": "GetById",
        "line_items": [{"product_id": pid, "qty": 1}]
    })
    assert created.status_code in (200, 201), created.text
    sale = created.json()

    # Fetch by ID
    got = client.get(f"/sales/{sale['id']}")
    assert got.status_code == 200
    data = got.json()
    assert data["id"] == sale["id"]
    assert data["customer_name"] == "GetById"
    assert isinstance(data.get("line_items"), list)
