import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.modules.ai.chains.market_analysis_chain import build_chain
from app.modules.ai.loaders.analytics_loader import load_analytics


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3)
    lang: str = Field("cs", pattern="^(cs|en|ru)$")


class AskResponse(BaseModel):
    answer: str


router = APIRouter()


@router.post("/ai/ask", response_model=AskResponse)
def ask_ai(body: AskRequest) -> AskResponse:
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise HTTPException(status_code=400, detail="DEEPSEEK_API_KEY is not configured")
    analytics = load_analytics()
    chain = build_chain()
    try:
        answer = chain(analytics, body.question, body.lang)
    except Exception as exc:  # pragma: no cover - bubble up as 500 with message
        raise HTTPException(status_code=500, detail=str(exc))
    return AskResponse(answer=answer)
