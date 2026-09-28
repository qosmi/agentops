from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.models.tool_definition import ToolDefinition


class FakeLLMProvider(LLMProvider):
    def __init__(self, responses: list[AgentResponse]) -> None:
        self.responses = responses
        self.call_count = 0
        self.received_tools: list[list[ToolDefinition]] = []

    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
        tools: list[ToolDefinition],
    ) -> AgentResponse:
        self.received_tools.append(tools)

        if self.call_count >= len(self.responses):
            raise RuntimeError("FakeLLMProvider ran out of responses")

        response = self.responses[self.call_count]
        self.call_count += 1

        return response