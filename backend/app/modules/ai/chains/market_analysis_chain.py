import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.modules.ai.prompts.market_prompts import PROMPTS


def _make_llm(model: str | None = None, temperature: float = 0.2):
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required")

    base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    model_name = model or os.getenv("DEEPSEEK_MODEL") or "deepseek-chat"

    kwargs = {"model": model_name, "temperature": temperature}
    kwargs["api_key"] = api_key
    kwargs["base_url"] = base_url
    return ChatOpenAI(**kwargs)


def build_chain(model: str | None = None, temperature: float = 0.2):
    llm = _make_llm(model=model, temperature=temperature)

    def run(analytics: dict, question: str, lang: str = "cs") -> str:
        system_prompt = PROMPTS.get(lang, PROMPTS["en"])
        system = SystemMessage(content=system_prompt)
        regions = analytics.get("regions") or []
        categories = analytics.get("categories") or []
        prices = analytics.get("prices") or []

        # Limit payload size to avoid context overflow
        user_payload = {
            "overview": analytics.get("overview"),
            "regions": regions[:50],
            "regions_total": len(regions),
            "categories": categories[:50],
            "categories_total": len(categories),
            "prices_sample": prices[:50],
            "prices_total": len(prices),
            "currency": "RUB",
            "question": question,
        }
        human = HumanMessage(content=str(user_payload))
        resp = llm.invoke([system, human])
        return resp.content

    return run
