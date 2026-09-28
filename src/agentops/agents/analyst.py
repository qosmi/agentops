from agentops.llm.base import LLMProvider


class AnalystAgent:
    def __init__(self, llm: LLMProvider) -> None:
        self.llm = llm

    def analyze(self, question: str) -> str:
        response = self.llm.generate(
            system_prompt="You are a business analyst.",
            messages=[
                {
                    "role": "user",
                    "content": question,
                }
            ],
        )

        return response.message