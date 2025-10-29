from fastapi import FastAPI
from src.app.routers import utils as utils_router

# PUBLIC_INTERFACE
def register_seed_endpoint(app: FastAPI) -> None:
    """Register the seed endpoint for inserting sample data."""
    app.include_router(utils_router.router, tags=["health", "utilities"])
