from typing import Any

from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.tools.registry import ToolRegistry


class AgentLoop:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolRegistry,
    ) -> None:
        self.llm = llm
        self.tools = tools

    def run(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        messages: list[dict[str, str]] = [
            {
                "role": "user",
                "content": user_message,
            }
        ]

        while True:
            response: AgentResponse = self.llm.generate(
                system_prompt=system_prompt,
                messages=messages,
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool = self.tools.get(
                        tool_call.tool_name
                    )

                    result: Any = tool.execute(
                        tool_call.arguments
                    )

                    messages.append(
                        {
                            "role": "assistant",
                            "content": response.message,
                        }
                    )

                    messages.append(
                        {
                            "role": "tool",
                            "content": str(result),
                        }
                    )

                continue

            return response.message