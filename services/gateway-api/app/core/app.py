from fastapi import FastAPI
from app.api.v1.router import api_router as v1_router
from app.api.errors.handlers import register_exception_handlers

def create_app() -> FastAPI:
    app = FastAPI(title="Decision Platform")

    app.include_router(v1_router)

    register_exception_handlers(app)

    return app
