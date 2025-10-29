# Backend Tests

Prerequisites:
- Running MySQL accessible per backend `.env.example` (default port 5001)
- Tables will be auto-created on app startup

Run:
```
cd sales-and-inventory-management-system-182200-182211/backend
pip install -r requirements.txt
pytest -q
```

Notes:
- Some tests are tolerant to existing data (idempotent `POST /seed`).
- Monetary fields are validated with two decimal rounding (half-up).
