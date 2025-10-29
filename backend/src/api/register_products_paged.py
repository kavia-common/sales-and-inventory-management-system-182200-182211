from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from src.app.db import get_db
from src.app import models, schemas


# PUBLIC_INTERFACE
def register_products_paged(app: FastAPI) -> None:
    """Register a simple paged products listing under /products/paged."""
    @app.get("/products/paged", response_model=list[schemas.ProductOut], tags=["products"], summary="List products (paged)")
    def products_paged(
        limit: int = Query(50, ge=1, le=200),
        offset: int = Query(0, ge=0),
        db: Session = Depends(get_db),
    ):
        """This is a public function."""
        q = db.query(models.Product).order_by(models.Product.id.desc()).limit(limit).offset(offset)
        return q.all()
