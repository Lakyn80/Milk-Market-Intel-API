from fastapi import APIRouter
import logging

from app.modules.monitoring.health import router as health_router
from app.modules.companies.api import router as companies_router

# AI router is optional; skip if langchain deps are not installed (e.g., CI without extras)
try:
    from app.modules.ai.api.ai_router import router as ai_router
except ImportError:
    ai_router = None
    logging.getLogger(__name__).warning("AI router disabled: langchain/openai not installed")

api_router = APIRouter()

api_router.include_router(health_router, prefix="/api/v1")
api_router.include_router(companies_router, prefix="/api/v1")
if ai_router:
    api_router.include_router(ai_router, prefix="/api/v1")
