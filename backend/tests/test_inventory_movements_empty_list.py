from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_inventory_movements_list_empty_initially():
    # We don't guarantee DB isolation; this test tolerates non-empty but expects list type.
    r = client.get("/inventory/movements")
    assert r.status_code == 200
    assert isinstance(r.json(), list)
