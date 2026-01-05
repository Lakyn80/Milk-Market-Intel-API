import argparse

from dotenv import load_dotenv

from app.modules.ai.chains.market_analysis_chain import build_chain
from app.modules.ai.loaders.analytics_loader import load_analytics


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LangChain MVP for analytics interpretation")
    parser.add_argument("--question", required=True, help="Question to ask about the analytics data")
    parser.add_argument("--lang", choices=["cs", "en", "ru"], default="cs", help="Language of the answer")
    parser.add_argument("--model", default=None, help="LLM model name (optional override)")
    return parser.parse_args()


def main() -> None:
    load_dotenv()
    args = parse_args()
    data = load_analytics()
    chain = build_chain(model=args.model, temperature=0.2)
    answer = chain(data, args.question, args.lang)
    print(answer)


if __name__ == "__main__":
    main()
