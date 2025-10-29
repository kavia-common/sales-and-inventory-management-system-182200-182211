from fastapi import FastAPI
from src.api.openapi_route import router as openapi_router

# PUBLIC_INTERFACE
def register_openapi_route(app: FastAPI) -> None:
    """This is a public function."""
    app.include_router(openapi_router)
