from typing import List

from app.modules.ai.langgraph.state import GraphState


def _match_regions(question: str, region_names: List[str]) -> List[str]:
    q = question.lower()
    matches = []
    for name in region_names:
        if isinstance(name, str) and name.lower() in q:
            matches.append(name)
    return list(dict.fromkeys(matches))  # dedupe preserve order


def route_intent(state: GraphState) -> GraphState:
    question = state.get("question", "")
    data = state.get("data") or {}
    regions_data = data.get("regions") or []
    region_names = [
        r.get("region")
        for r in regions_data
        if isinstance(r, dict) and isinstance(r.get("region"), str)
    ]
    matched = _match_regions(question, region_names)

    intent = "market_overview"
    if len(matched) >= 2:
        intent = "compare_regions"
    elif len(matched) == 1:
        intent = "region_overview"

    state["intent"] = intent
    return state
