from langgraph.graph import END, StateGraph

from app.modules.ai.langgraph.state import GraphState
from app.modules.ai.langgraph.nodes.load_data import load_data
from app.modules.ai.langgraph.nodes.route_intent import route_intent
from app.modules.ai.langgraph.nodes.select_context import select_context
from app.modules.ai.langgraph.nodes.summarize import summarize


def build_graph() -> StateGraph:
    graph = StateGraph(GraphState)
    graph.add_node("load_data", load_data)
    graph.add_node("route_intent", route_intent)
    graph.add_node("select_context", select_context)
    graph.add_node("summarize", summarize)

    graph.set_entry_point("load_data")
    graph.add_edge("load_data", "route_intent")
    graph.add_edge("route_intent", "select_context")
    graph.add_edge("select_context", "summarize")
    graph.add_edge("summarize", END)
    return graph
