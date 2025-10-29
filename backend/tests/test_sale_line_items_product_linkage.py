from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sale_line_items_include_product_id_on_get():
    client.post("/seed")
    products = client.get("/products").json()
    if len(products) < 1:
        return
    pid = products[0]["id"]
    sale = client.post("/sales", json={"customer_name": "Linkage", "line_items": [{"product_id": pid, "qty": 1}]}).json()
    got = client.get(f"/sales/{sale['id']}")
    assert got.status_code == 200
    data = got.json()
    assert data["line_items"]
    assert data["line_items"][0]["product_id"] == pid
