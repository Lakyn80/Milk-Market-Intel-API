from fastapi import APIRouter
from app.modules.monitoring.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router, prefix="/api/v1", tags=["health"])
