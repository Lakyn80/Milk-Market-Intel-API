import argparse
import json

from dotenv import load_dotenv

from app.modules.ai.langgraph.graph import build_graph
from app.modules.ai.langgraph.state import GraphState


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LangGraph MVP over precomputed analytics")
    parser.add_argument("--question", required=True, help="Question to ask")
    parser.add_argument("--lang", choices=["cs", "en", "ru"], default="cs", help="Answer language")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()

    graph = build_graph().compile()
    initial_state: GraphState = {"question": args.question, "lang": args.lang}
    result = graph.invoke(initial_state)

    print(f"Intent: {result.get('intent')}")
    context = result.get("context") or {}
    context_keys = ", ".join(context.keys())
    print(f"Context keys: {context_keys}")
    print("Answer:")
    print(result.get("answer", ""))


if __name__ == "__main__":
    main()
