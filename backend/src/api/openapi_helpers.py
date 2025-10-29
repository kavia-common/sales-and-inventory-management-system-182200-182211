from fastapi import FastAPI
from fastapi.responses import JSONResponse


# PUBLIC_INTERFACE
def register_openapi_route(app: FastAPI) -> None:
    """Register an explicit /openapi.json route for environments that do not serve it by default."""
    @app.get("/openapi.json", include_in_schema=False)
    def openapi_json():
        """This is a public function."""
        return JSONResponse(app.openapi())


# PUBLIC_INTERFACE
def register_debug_routes(app: FastAPI) -> None:
    """Register lightweight debug routes used by CI or diagnostics."""
    @app.get("/debug/ping", tags=["health"], summary="Ping", description="Simple ping endpoint")
    def ping():
        """This is a public function."""
        return {"pong": True}
