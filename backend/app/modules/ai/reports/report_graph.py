from typing import Any, Dict

from langgraph.graph import END, StateGraph

from app.modules.ai.reports.report_nodes import (
    node_category_deep_dive,
    node_market_overview,
    node_region_comparison,
)
from app.modules.ai.reports.report_types import ReportType
from app.modules.ai.reports.report_context import build_context


State = Dict[str, Any]


def _select_report(state: State) -> str:
    report_type = state.get("type")
    if report_type == ReportType.REGION_COMPARISON:
        return "region_comparison"
    if report_type == ReportType.CATEGORY_DEEP_DIVE:
        return "category_deep_dive"
    return "market_overview"


def _set_context(state: State) -> State:
    state["context"] = build_context(state["request"])
    return state


def build_graph() -> StateGraph:
    graph = StateGraph(State)
    graph.add_node("set_context", _set_context)
    graph.add_node("market_overview", node_market_overview)
    graph.add_node("region_comparison", node_region_comparison)
    graph.add_node("category_deep_dive", node_category_deep_dive)

    graph.set_entry_point("set_context")
    graph.add_conditional_edges(
        "set_context",
        _select_report,
        {
            "market_overview": "market_overview",
            "region_comparison": "region_comparison",
            "category_deep_dive": "category_deep_dive",
        },
    )
    graph.add_edge("market_overview", END)
    graph.add_edge("region_comparison", END)
    graph.add_edge("category_deep_dive", END)
    return graph
