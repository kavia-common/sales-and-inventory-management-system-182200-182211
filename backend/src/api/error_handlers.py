from fastapi import Request
from fastapi.responses import JSONResponse
import traceback


# PUBLIC_INTERFACE
async def unhandled_exception_handler(request: Request, exc: Exception):
    """Global handler for unhandled exceptions, returns 500 with minimal details."""
    # Note: Avoid leaking internal details in production; for now include brief info
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "path": request.url.path,
            "error": str(exc),
            "trace": traceback.format_exc().splitlines()[-1] if exc else "",
        },
    )
