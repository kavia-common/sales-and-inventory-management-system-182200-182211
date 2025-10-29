from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.db import get_db
from src.app import models

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/seed", summary="Seed sample data", description="Insert a few sample products if they do not already exist")
def seed(db: Session = Depends(get_db)):
    """This is a public function."""
    samples = [
        {"name": "Sample Pen", "sku": "SKU-PEN-001", "price": 10.00, "gst_rate": 18.0, "stock_qty": 100},
        {"name": "Sample Notebook", "sku": "SKU-NOTE-001", "price": 50.00, "gst_rate": 12.0, "stock_qty": 200},
        {"name": "Sample Stapler", "sku": "SKU-STAP-001", "price": 150.00, "gst_rate": 18.0, "stock_qty": 50},
    ]
    created = 0
    for s in samples:
        exists = db.query(models.Product).filter(models.Product.sku == s["sku"]).first()
        if not exists:
            p = models.Product(**s)
            db.add(p)
            created += 1
    return {"inserted": created}
