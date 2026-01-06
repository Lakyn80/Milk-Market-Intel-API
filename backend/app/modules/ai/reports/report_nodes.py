import os
from typing import Any, Dict

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from app.modules.ai.reports.report_prompts import PROMPTS
from app.modules.ai.reports.report_types import ReportType


def _make_llm():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required")
    base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    return ChatOpenAI(model=model, temperature=0.2, api_key=api_key, base_url=base_url)


def _summarize(context: Dict[str, Any], lang: str, report_type: ReportType) -> str:
    llm = _make_llm()
    prompt = PROMPTS[report_type.value].get(lang, PROMPTS[report_type.value]["en"])
    system = SystemMessage(content=prompt)
    human = HumanMessage(content=str(context))
    resp = llm.invoke([system, human])
    return resp.content


def node_market_overview(state: Dict[str, Any]) -> Dict[str, Any]:
    state["report_text"] = _summarize(state.get("context") or {}, state.get("lang", "cs"), ReportType.MARKET_OVERVIEW)
    state["meta"] = {"type": ReportType.MARKET_OVERVIEW.value}
    return state


def node_region_comparison(state: Dict[str, Any]) -> Dict[str, Any]:
    state["report_text"] = _summarize(state.get("context") or {}, state.get("lang", "cs"), ReportType.REGION_COMPARISON)
    state["meta"] = {"type": ReportType.REGION_COMPARISON.value}
    return state


def node_category_deep_dive(state: Dict[str, Any]) -> Dict[str, Any]:
    state["report_text"] = _summarize(state.get("context") or {}, state.get("lang", "cs"), ReportType.CATEGORY_DEEP_DIVE)
    state["meta"] = {"type": ReportType.CATEGORY_DEEP_DIVE.value}
    return state
