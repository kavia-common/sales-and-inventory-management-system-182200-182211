from fastapi import FastAPI
from .log_startup import log_startup

# PUBLIC_INTERFACE
def register_startup_hooks(app: FastAPI) -> None:
    """This is a public function."""
    @app.on_event("startup")
    def _log():
        log_startup()
