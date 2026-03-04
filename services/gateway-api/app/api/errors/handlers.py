import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.domain.exceptions import IdempotencyConflict
from app.core.config import settings

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(IdempotencyConflict)
    async def idempotency_conflict_handler(request: Request, exc: IdempotencyConflict):
        return JSONResponse(status_code=409, content={"detail": "Idempotency key reused with different payload"})

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Unhandled error", extra={"path": str(request.url.path), "method": request.method})

        # Prevent leaking internal things in prod
        if settings.environment == "dev":
            raise exc
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
