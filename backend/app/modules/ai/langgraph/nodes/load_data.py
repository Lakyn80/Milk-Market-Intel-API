from app.modules.ai.loaders.analytics_loader import load_analytics
from app.modules.ai.langgraph.state import GraphState


def load_data(state: GraphState) -> GraphState:
    data = load_analytics()
    state["data"] = data
    return state
