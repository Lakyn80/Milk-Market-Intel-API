from fastapi import APIRouter, HTTPException
import logging

from app.modules.monitoring.health import router as health_router
from app.modules.companies.api import router as companies_router

# AI router is optional; provide a stub if deps are missing to avoid 404s.
try:
    from app.modules.ai.api.ai_router import router as ai_router
except ImportError:
    logging.getLogger(__name__).warning("AI router disabled: langchain/openai not installed")
    ai_router = APIRouter()

    @ai_router.post("/ai/ask")
    def ai_disabled() -> None:
        raise HTTPException(
            status_code=503,
            detail="AI router disabled: langchain/openai not installed",
        )

try:
    from app.modules.ai.api.report_router import router as report_router
except ImportError:
    logging.getLogger(__name__).warning("Report router disabled: langchain/openai not installed")
    report_router = APIRouter()

    @report_router.post("/reports/build")
    def reports_disabled() -> None:
        raise HTTPException(
            status_code=503,
            detail="Report router disabled: langchain/openai not installed",
        )

api_router = APIRouter()

api_router.include_router(health_router, prefix="/api/v1")
api_router.include_router(companies_router, prefix="/api/v1")
if ai_router:
    api_router.include_router(ai_router, prefix="/api/v1")
if report_router:
    api_router.include_router(report_router, prefix="/api/v1")
