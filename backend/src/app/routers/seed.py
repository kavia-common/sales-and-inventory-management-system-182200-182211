from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models

router = APIRouter()


# PUBLIC_INTERFACE
@router.post("/", summary="Seed sample data", description="Insert initial products if they do not exist. Idempotent.")
def seed(db: Session = Depends(get_db)):
    """This is a public function."""
    # Define baseline products
    samples = [
        {"name": "Notebook A5 Ruled", "sku": "NB-A5-R-001", "price": 50.00, "gst_rate": 18.00, "stock_qty": 200},
        {"name": "Gel Pen Blue", "sku": "PEN-GEL-BLU-001", "price": 10.00, "gst_rate": 12.00, "stock_qty": 500},
        {"name": "Stapler Medium", "sku": "STAP-MED-001", "price": 120.00, "gst_rate": 18.00, "stock_qty": 80},
    ]
    created = 0
    for p in samples:
        exists = db.query(models.Product).filter(models.Product.sku == p["sku"]).first()
        if not exists:
            obj = models.Product(**p)
            db.add(obj)
            created += 1
    # Let session commit via dependency
    return {"status": "ok", "created": created}
