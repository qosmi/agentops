from typing import Any

from agentops.llm.base import LLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.models.agent_state import AgentState
from agentops.models.tool_definition import ToolDefinition
from agentops.observability.events import AgentEvent
from agentops.observability.logger import AgentLogger
from agentops.tools.registry import ToolRegistry


class AgentLoop:
    def __init__(
        self,
        llm: LLMProvider,
        tools: ToolRegistry,
        config: AgentConfig | None = None,
        logger: AgentLogger | None = None,
    ) -> None:
        if config is None:
            config = AgentConfig()

        self.llm = llm
        self.tools = tools
        self.config = config
        self.logger = logger or AgentLogger()

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

        self._record_event(
            state=state,
            event_type="agent_started",
            data={
                "user_message": user_message,
            },
        )

        while state.iteration < self.config.max_iterations:
            tool_definitions = [
                ToolDefinition(
                    name=tool.name,
                    description=tool.description,
                )
                for tool in self.tools.list()
                if tool.name in self.config.allowed_tools
            ]

            self._record_event(
                state=state,
                event_type="llm_request",
                data={
                    "available_tools": [
                        tool.name
                        for tool in tool_definitions
                    ],
                },
            )

            response: AgentResponse = self.llm.generate(
                system_prompt=state.system_prompt,
                messages=state.messages,
                tools=tool_definitions,
            )

            state.iteration += 1

            state.llm_usage = state.llm_usage.add(
                response.usage
            )

            self._record_event(
                state=state,
                event_type="llm_response",
                data={
                    "tool_call_count": len(
                        response.tool_calls
                    ),
                    "input_tokens": (
                        response.usage.input_tokens
                    ),
                    "output_tokens": (
                        response.usage.output_tokens
                    ),
                    "total_tokens": (
                        response.usage.total_tokens
                    ),
                    "estimated_cost_usd": str(
                        response.usage.estimated_cost_usd
                    ),
                },
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    if (
                        tool_call.tool_name
                        not in self.config.allowed_tools
                    ):
                        self._record_event(
                            state=state,
                            event_type="tool_denied",
                            data={
                                "tool_name": (
                                    tool_call.tool_name
                                ),
                            },
                        )

                        raise PermissionError(
                            f"Tool not allowed: "
                            f"{tool_call.tool_name}"
                        )

                    self._record_event(
                        state=state,
                        event_type="tool_started",
                        data={
                            "tool_name": (
                                tool_call.tool_name
                            ),
                            "arguments": (
                                tool_call.arguments
                            ),
                        },
                    )

                    tool = self.tools.get(
                        tool_call.tool_name
                    )

                    result: Any = tool.execute(
                        tool_call.arguments
                    )

                    self._record_event(
                        state=state,
                        event_type="tool_completed",
                        data={
                            "tool_name": (
                                tool_call.tool_name
                            ),
                        },
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

            self._record_event(
                state=state,
                event_type="agent_completed",
                data={
                    "total_iterations": state.iteration,
                    "input_tokens": (
                        state.llm_usage.input_tokens
                    ),
                    "output_tokens": (
                        state.llm_usage.output_tokens
                    ),
                    "total_tokens": (
                        state.llm_usage.total_tokens
                    ),
                    "estimated_cost_usd": str(
                        state.llm_usage.estimated_cost_usd
                    ),
                },
            )

            return state.final_answer

        self._record_event(
            state=state,
            event_type="agent_failed",
            data={
                "reason": "maximum_iterations_exceeded",
                "max_iterations": (
                    self.config.max_iterations
                ),
            },
        )

        raise RuntimeError(
            f"Agent exceeded maximum iterations: "
            f"{self.config.max_iterations}"
        )

    def _record_event(
        self,
        state: AgentState,
        event_type: str,
        data: dict[str, Any],
    ) -> None:
        event = AgentEvent(
            event_type=event_type,
            iteration=state.iteration,
            data=data,
        )

        state.events.append(event)
        self.logger.log(event)