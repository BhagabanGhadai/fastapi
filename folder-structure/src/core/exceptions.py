from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Base for all domain errors. Services raise these; the handler maps to HTTP."""

    status_code = 500
    detail = "Internal server error"

    def __init__(self, detail: str | None = None):
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class NotFound(AppError):
    status_code = 404
    detail = "Not found"


class Conflict(AppError):
    status_code = 409
    detail = "Conflict"


class Unauthorized(AppError):
    status_code = 401
    detail = "Unauthorized"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
