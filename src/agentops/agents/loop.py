from typing import Any

from agentops.llm.base import LLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.models.agent_state import AgentState
from agentops.tools.registry import ToolRegistry


class AgentLoop:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolRegistry,
        config: AgentConfig | None = None,
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.config = config or AgentConfig()

        if self.config.max_iterations < 1:
            raise ValueError("max_iterations must be at least 1")

    def run(
        self,
        system_prompt: str,
        user_message: str,
    ) -> str:
        state = AgentState(
            system_prompt=system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
        )

        while state.iteration < self.config.max_iterations:
            response: AgentResponse = self.llm.generate(
                system_prompt=state.system_prompt,
                messages=state.messages,
            )

            state.iteration += 1

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if (
                        tool_call.tool_name
                        not in self.config.allowed_tools
                    ):
                        raise PermissionError(
                            f"Tool not allowed: {tool_call.tool_name}"
                        )

                    tool = self.tools.get(tool_call.tool_name)

                    result: Any = tool.execute(
                        tool_call.arguments
                    )

                    state.messages.append(
                        {
                            "role": "assistant",
                            "content": response.message,
                        }
                    )

                    state.messages.append(
                        {
                            "role": "tool",
                            "content": str(result),
                        }
                    )

                continue

            state.final_answer = response.message
            return state.final_answer

        raise RuntimeError(
            "Agent exceeded maximum iterations: {self.config.max_iterations}"
        )