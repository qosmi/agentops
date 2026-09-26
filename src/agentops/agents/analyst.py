from agentops.llm.base import LLMProvider


class AnalystAgent:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def analyze(self, question: str) -> str:
        system_prompt = """
You are a business data analyst.

Analyze the user's question carefully.
Do not invent data.
If evidence is unavailable, say so.
""".strip()

        return self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=question,
        )