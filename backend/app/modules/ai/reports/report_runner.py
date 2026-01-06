import argparse

from dotenv import load_dotenv

from app.modules.ai.reports.report_graph import build_graph
from app.modules.ai.reports.report_types import ReportRequest, ReportType


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Report builder MVP (LangGraph)")
    parser.add_argument("--type", required=True, choices=[t.value for t in ReportType], help="Report type")
    parser.add_argument("--lang", choices=["cs", "en", "ru"], default="cs", help="Language")
    parser.add_argument("--regions", nargs="*", help="Regions (strings or numbers)")
    parser.add_argument("--category", help="Category for deep dive")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    req = ReportRequest(type=args.type, lang=args.lang, regions=args.regions, category=args.category)
    graph = build_graph().compile()
    result = graph.invoke({"type": req.type, "lang": req.lang, "request": req})
    print("Intent/report:", req.type)
    meta = result.get("meta")
    if meta:
        print("Meta:", meta)
    print("Report:")
    print(result.get("report_text", ""))


if __name__ == "__main__":
    main()
