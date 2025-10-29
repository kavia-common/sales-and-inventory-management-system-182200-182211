from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from decimal import Decimal

from src.app.db import get_db
from src.app import models

router = APIRouter()


def _ensure_product(db: Session, sku: str, name: str, price: Decimal, gst_rate: Decimal, stock_qty: int) -> models.Product:
    prod = db.query(models.Product).filter(models.Product.sku == sku).first()
    if prod:
        return prod
    prod = models.Product(
        name=name,
        sku=sku,
        price=price,
        gst_rate=gst_rate,
        stock_qty=stock_qty,
    )
    db.add(prod)
    db.flush()
    db.refresh(prod)
    return prod


# PUBLIC_INTERFACE
@router.post("/seed", summary="Seed sample data", description="Insert sample products if not already present. Idempotent.", tags=["health"])
def seed(db: Session = Depends(get_db)):
    """This is a public function."""
    items = [
        ("SKU-001", "Sample Product A", Decimal("10.00"), Decimal("5.00"), 100),
        ("SKU-002", "Sample Product B", Decimal("25.50"), Decimal("12.00"), 200),
        ("SKU-003", "Sample Product C", Decimal("5.75"), Decimal("18.00"), 300),
    ]
    created = []
    for sku, name, price, gst, qty in items:
        prod = _ensure_product(db, sku, name, price, gst, qty)
        created.append({"id": prod.id, "sku": prod.sku})
    return {"status": "ok", "products": created}
