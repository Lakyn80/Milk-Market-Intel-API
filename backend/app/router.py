from fastapi import APIRouter
from app.modules.monitoring.health import router as health_router
from app.modules.companies.api import router as companies_router
from app.modules.ai.api.ai_router import router as ai_router

api_router = APIRouter()

api_router.include_router(health_router, prefix="/api/v1")
api_router.include_router(companies_router, prefix="/api/v1")
api_router.include_router(ai_router, prefix="/api/v1")
