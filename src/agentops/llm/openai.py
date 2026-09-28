import json
import os
from typing import Any

from openai import OpenAI

from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.models.tool_call import ToolCall


class OpenAILLMProvider(LLMProvider):
    def __init__(
        self,
        model: str = "gpt-5-mini",
    ) -> None:
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"]
        )
        self.model = model

    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
    ) -> AgentResponse:
        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=messages,
        )

        return AgentResponse(
            message=response.output_text,
            tool_calls=[],
        )