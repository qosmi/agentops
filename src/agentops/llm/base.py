from abc import ABC, abstractmethod

from agentops.models.agent_response import AgentResponse


class LLMProvider(ABC):
    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> AgentResponse:
        raise NotImplementedError