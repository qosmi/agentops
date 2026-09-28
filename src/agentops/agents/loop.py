from typing import Any

from agentops.llm.base import LLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.models.agent_state import AgentState
from agentops.tools.registry import ToolRegistry


class AgentLoop:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolRegistry,
        max_iterations: int = 5,
    ) -> None:
        if max_iterations < 1:
            raise ValueError("max_iterations must be at least 1")

        self.llm = llm
        self.tools = tools
        self.max_iterations = max_iterations

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

        while state.iteration < self.max_iterations:
            response: AgentResponse = self.llm.generate(
                system_prompt=state.system_prompt,
                messages=state.messages,
            )

            state.iteration += 1

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    tool = self.tools.get(
                        tool_call.tool_name
                    )

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
            f"Agent exceeded maximum iterations: {self.max_iterations}"
        )