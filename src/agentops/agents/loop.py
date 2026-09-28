from typing import Any

from agentops.llm.base import LLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_observation import AgentObservation
from agentops.models.agent_response import AgentResponse
from agentops.models.agent_state import AgentState
from agentops.models.evidence import Evidence
from agentops.models.tool_definition import ToolDefinition
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

        tool_definitions = [
            ToolDefinition(
                name=tool.name,
                description=tool.description,
            )
            for tool in self.tools.list()
            if tool.name in self.config.allowed_tools
        ]

        while state.iteration < self.config.max_iterations:
            response: AgentResponse = self.llm.generate(
                system_prompt=state.system_prompt,
                messages=state.messages,
                tools=tool_definitions,
            )

            state.iteration += 1

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if tool_call.tool_name not in self.config.allowed_tools:
                        raise PermissionError(
                            f"Tool not allowed: {tool_call.tool_name}"
                        )

                    tool = self.tools.get(tool_call.tool_name)

                    result: Any = tool.execute(
                        tool_call.arguments
                    )

                    observation = AgentObservation(
                        iteration=state.iteration,
                        tool_name=tool_call.tool_name,
                        arguments=tool_call.arguments,
                        result=result,
                    )

                    state.observations.append(observation)

                    state.evidence.append(
                        Evidence(
                            source=tool_call.tool_name,
                            value=result,
                        )
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
            f"Agent exceeded maximum iterations: "
            f"{self.config.max_iterations}"
        )