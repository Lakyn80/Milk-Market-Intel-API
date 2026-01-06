from typing import Any, Dict, List

from app.modules.ai.langgraph.state import GraphState


def select_context(state: GraphState) -> GraphState:
    intent = state.get("intent") or "market_overview"
    data = state.get("data") or {}
    regions: List[Dict[str, Any]] = data.get("regions") or []

    context: Dict[str, Any] = {}
    if intent == "compare_regions":
        question = state.get("question", "").lower()
        matched = [
            r for r in regions
            if isinstance(r, dict) and r.get("region") and r.get("region").lower() in question
        ]
        context["regions"] = matched[:2]
    elif intent == "region_overview":
        question = state.get("question", "").lower()
        matched = [
            r for r in regions
            if isinstance(r, dict) and r.get("region") and r.get("region").lower() in question
        ]
        context["regions"] = matched[:1]
    else:
        context["regions_sample"] = regions[:10]

    context["overview"] = data.get("overview")
    context["categories_sample"] = (data.get("categories") or [])[:10]
    context["prices_sample"] = (data.get("prices") or [])[:10]

    state["context"] = context
    return state
