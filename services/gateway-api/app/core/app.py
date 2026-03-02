from fastapi import FastAPI
from app.api.v1.router import api_router

def create_app() -> FastAPI:
    app = FastAPI(title="Decision Platform")

    app.include_router(api_router)

    return app
