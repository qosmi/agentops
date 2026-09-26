from agentops.llm.base import LLMProvider


class FakeLLMProvider(LLMProvider):
    def __init__(self, response: str) -> None:
        self.response = response

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        return self.response