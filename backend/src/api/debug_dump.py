from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.app.db import get_db
from src.app import models

router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/debug/products", tags=["health"], summary="Debug products dump", description="Return a raw dump of products for debugging")
def debug_products(db: Session = Depends(get_db)):
    """This is a public function."""
    rows = db.query(models.Product).order_by(models.Product.id.asc()).all()
    return [
        {
            "id": r.id,
            "name": r.name,
            "sku": r.sku,
            "price": str(r.price),
            "gst_rate": str(r.gst_rate),
            "stock_qty": r.stock_qty,
        }
        for r in rows
    ]
