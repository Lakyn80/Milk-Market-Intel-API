from fastapi import APIRouter
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
    analytics = load_analytics()
    chain = build_chain()
    answer = chain(analytics, body.question, body.lang)
    return AskResponse(answer=answer)
