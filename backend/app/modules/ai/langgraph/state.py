from typing import Any, Dict, Optional, TypedDict


class GraphState(TypedDict, total=False):
    question: str
    lang: str
    intent: Optional[str]
    data: Optional[Dict[str, Any]]
    context: Optional[Dict[str, Any]]
    answer: Optional[str]
