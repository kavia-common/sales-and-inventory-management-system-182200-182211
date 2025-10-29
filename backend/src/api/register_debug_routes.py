from fastapi import FastAPI
from src.api import debug_dump

# PUBLIC_INTERFACE
def register_debug_routes(app: FastAPI) -> None:
    """This is a public function."""
    app.include_router(debug_dump.router)
