from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_products_create_delete_consistency():
    # Create three products
    ids = []
    for i in range(3):
        r = client.post("/products", json={
            "name": f"CD-{i}",
            "sku": f"CD-SKU-{i}",
            "price": 2.5 + i,
            "gst_rate": 5.0,
            "stock_qty": 1 + i
        })
        assert r.status_code in (200, 201), r.text
        ids.append(r.json()["id"])

    # Delete the middle one
    d = client.delete(f"/products/{ids[1]}")
    assert d.status_code == 204

    # List and ensure only the remaining ones are present
    lst = client.get("/products")
    assert lst.status_code == 200
    got_ids = {p["id"] for p in lst.json()}
    assert ids[1] not in got_ids
    assert ids[0] in got_ids
    assert ids[2] in got_ids
