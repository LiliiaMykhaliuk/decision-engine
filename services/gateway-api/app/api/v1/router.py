from fastapi import APIRouter
from .decisions import router as decisions_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(decisions_router, prefix="/decisions")
