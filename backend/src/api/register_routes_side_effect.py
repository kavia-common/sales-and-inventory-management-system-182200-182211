from fastapi import FastAPI
from .register_routes import register_app_routes
from .register_utils_seed import register_seed_endpoint

# PUBLIC_INTERFACE
def apply_all_routes(app: FastAPI) -> None:
    """Apply all routers including utilities/seed."""
    register_app_routes(app)
    register_seed_endpoint(app)
