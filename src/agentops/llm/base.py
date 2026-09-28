from abc import ABC, abstractmethod

from agentops.models.agent_response import AgentResponse
from agentops.models.tool_definition import ToolDefinition


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
        tools: list[ToolDefinition],
    ) -> AgentResponse:
        raise NotImplementedError