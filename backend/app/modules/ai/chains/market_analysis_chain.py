from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from app.modules.ai.prompts.market_prompts import PROMPTS


def build_chain(model_name: str = "gpt-3.5-turbo", temperature: float = 0.2):
    llm = ChatOpenAI(model=model_name, temperature=temperature)

    def run(analytics: dict, question: str, lang: str = "cs") -> str:
        prompt = PROMPTS.get(lang, PROMPTS["en"])
        system = SystemMessage(content=prompt)
        # We pass analytics dict as-is; LLM must not recalc, only interpret.
        user_content = f"Analytics data:\n{analytics}\n\nQuestion:\n{question}"
        human = HumanMessage(content=user_content)
        resp = llm([system, human])
        return resp.content

    return run
