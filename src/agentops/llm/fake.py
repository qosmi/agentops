from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse


class FakeLLMProvider(LLMProvider):
    def __init__(
        self,
        responses: list[AgentResponse],
    ) -> None:
        self.responses = responses
        self.call_count = 0

    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> AgentResponse:
        if self.call_count >= len(self.responses):
            raise RuntimeError(
                "FakeLLMProvider ran out of responses"
            )

        response = self.responses[self.call_count]
        self.call_count += 1

        return response