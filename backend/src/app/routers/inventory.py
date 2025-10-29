from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.app.db import get_db
from src.app import models, schemas

router = APIRouter()


# PUBLIC_INTERFACE
@router.post(
    "/movements",
    response_model=schemas.InventoryMovementOut,
    summary="Create inventory movement",
    description="Record an inventory movement that adjusts product stock quantity (positive to add, negative to remove).",
)
def create_movement(payload: schemas.InventoryMovementCreate, db: Session = Depends(get_db)):
    """This is a public function."""
    product = db.query(models.Product).get(payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock_qty = int(product.stock_qty) + int(payload.change_qty)
    move = models.InventoryMovement(
        product_id=payload.product_id,
        change_qty=payload.change_qty,
        reason=payload.reason,
    )
    db.add(product)
    db.add(move)
    db.flush()
    db.refresh(move)
    return move


# PUBLIC_INTERFACE
@router.get("/movements", response_model=List[schemas.InventoryMovementOut], summary="List inventory movements", description="List inventory movements ordered by latest first")
def list_movements(db: Session = Depends(get_db)):
    """This is a public function."""
    return db.query(models.InventoryMovement).order_by(models.InventoryMovement.timestamp.desc()).all()
