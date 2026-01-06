import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.modules.ai.reports.report_graph import build_graph
from app.modules.ai.reports.report_types import ReportRequest


class ReportResponse(BaseModel):
    report_text: str
    meta: dict


router = APIRouter()

# compile graph once
_graph = build_graph().compile()


@router.post("/reports/build", response_model=ReportResponse)
def build_report(body: ReportRequest) -> ReportResponse:
    try:
        result = _graph.invoke({"type": body.type, "lang": body.lang, "request": body})
        return ReportResponse(report_text=result.get("report_text", ""), meta=result.get("meta", {}))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as exc:  # pragma: no cover - bubble up unknown errors
        logging.getLogger(__name__).exception("Report build failed")
        raise HTTPException(status_code=500, detail=str(exc))
