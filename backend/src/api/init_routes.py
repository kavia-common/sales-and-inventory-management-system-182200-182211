from src.api.main import app
from src.api.register_routes_side_effect import apply_all_routes

# PUBLIC_INTERFACE
def init_routes():
    """Initialize and register all routers."""
    apply_all_routes(app)
    return app
