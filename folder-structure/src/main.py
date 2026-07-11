from fastapi import FastAPI

from src.domains.auth.router import router as auth_router
from src.core.exceptions import register_exception_handlers
from src.core.logging import setup_logging
from src.domains.users.router import router as users_router


def create_app() -> FastAPI:
    setup_logging()
    app = FastAPI(title="fastapi-project")
    register_exception_handlers(app)
    app.include_router(auth_router)
    app.include_router(users_router)

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
