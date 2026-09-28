import os
from typing import cast

from openai import OpenAI
from openai.types.responses import (
    FunctionToolParam,
    ResponseInputParam,
)

from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.models.tool_definition import ToolDefinition


class OpenAILLMProvider(LLMProvider):
    def __init__(self, model: str | None = None) -> None:
        self.client = OpenAI(
            api_key=os.environ["OPENAI_API_KEY"],
        )

        if model is not None:
            self.model = model
        else:
            configured_model = os.environ.get("OPENAI_MODEL")

            if configured_model is not None:
                self.model = configured_model
            else:
                self.model = "gpt-5"

    def generate(
        self,
        system_prompt: str,
        messages: list[dict[str, str]],
        tools: list[ToolDefinition],
    ) -> AgentResponse:
        openai_messages = [
            {
                "role": message["role"],
                "content": message["content"],
                "type": "message",
            }
            for message in messages
        ]

        openai_input = cast(
            ResponseInputParam,
            openai_messages,
        )

        openai_tools: list[FunctionToolParam] = [
            FunctionToolParam(
                type="function",
                name=tool.name,
                description=tool.description,
                parameters={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": True,
                },
                strict=False,
            )
            for tool in tools
        ]

        response = self.client.responses.create(
            model=self.model,
            instructions=system_prompt,
            input=openai_input,
            tools=openai_tools,
        )

        return AgentResponse(
            message=response.output_text,
        )