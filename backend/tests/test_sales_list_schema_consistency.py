from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_sales_list_schema_consistency():
    client.post("/seed")
    r = client.get("/sales")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    if data:
        assert "line_items" in data[0]
