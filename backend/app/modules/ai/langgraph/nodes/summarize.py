import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from app.modules.ai.langgraph.state import GraphState


def _make_llm():
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY is required")
    base_url = os.getenv("DEEPSEEK_API_BASE", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
    return ChatOpenAI(model=model, temperature=0.2, api_key=api_key, base_url=base_url)


PROMPTS = {
    "cs": "Jsi konzultant. Máš již spočítaná data. Neprováděj žádné výpočty, jen je interpretuj. Odpovídej česky.",
    "en": "You are a consultant. Data is precomputed. Do NOT calculate; only interpret. Answer in English.",
    "ru": "Ты консультант. Данные уже посчитаны. Не считай, только интерпретируй. Отвечай по-русски.",
}


def summarize(state: GraphState) -> GraphState:
    llm = _make_llm()
    lang = state.get("lang", "cs")
    system = SystemMessage(content=PROMPTS.get(lang, PROMPTS["en"]))
    human = HumanMessage(content=str({
        "question": state.get("question"),
        "intent": state.get("intent"),
        "context": state.get("context"),
    }))
    resp = llm.invoke([system, human])
    state["answer"] = resp.content
    return state
