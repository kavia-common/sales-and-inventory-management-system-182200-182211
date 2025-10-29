from fastapi import FastAPI

# Import routers from app package
from src.app.routers import products as products_router
from src.app.routers import inventory as inventory_router
from src.app.routers import sales as sales_router
from src.app.routers import invoices as invoices_router
from src.app.routers import utils as utils_router


# PUBLIC_INTERFACE
def register_app_routes(app: FastAPI) -> None:
    """Register core application routers on the provided FastAPI app."""
    app.include_router(products_router.router, prefix="/products", tags=["products"])
    app.include_router(inventory_router.router, prefix="/inventory", tags=["inventory"])
    app.include_router(sales_router.router, prefix="/sales", tags=["sales"])
    app.include_router(invoices_router.router, prefix="/invoices", tags=["invoices"])
    # seed and utility endpoints (no prefix)
    app.include_router(utils_router.router, tags=["health", "utilities"])
