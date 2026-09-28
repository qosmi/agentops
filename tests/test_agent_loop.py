import pandas as pd
import pytest

from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.models.tool_call import ToolCall
from agentops.tools.registry import ToolRegistry
from agentops.tools.resolution_time import ResolutionTimeTool


def create_registry() -> ToolRegistry:
    tickets = pd.DataFrame(
        [
            {
                "ticket_id": "1",
                "created_at": "2026-08-01T10:00:00",
                "closed_at": "2026-08-01T14:00:00",
                "product": "payments",
                "category": "bug",
                "priority": "high",
            },
            {
                "ticket_id": "2",
                "created_at": "2026-08-02T10:00:00",
                "closed_at": "2026-08-02T18:00:00",
                "product": "payments",
                "category": "bug",
                "priority": "low",
            },
        ]
    )

    registry = ToolRegistry()
    registry.register(ResolutionTimeTool(tickets))

    return registry


def test_agent_loop_calls_allowed_tool() -> None:
    registry = create_registry()

    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need data.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={"group_by": "product"},
                    )
                ],
            ),
            AgentResponse(message="Done."),
        ]
    )

    agent = AgentLoop(
        llm=llm,
        tools=registry,
        config=AgentConfig(
            max_iterations=5,
            allowed_tools={"get_resolution_time"},
        ),
    )

    result = agent.run(
        system_prompt="You are a business analyst.",
        user_message="Investigate resolution time.",
    )

    assert result == "Done."


def test_agent_loop_rejects_disallowed_tool() -> None:
    registry = create_registry()

    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I want to send an email.",
                tool_calls=[
                    ToolCall(
                        tool_name="send_email",
                        arguments={"recipient": "manager"},
                    )
                ],
            )
        ]
    )

    agent = AgentLoop(
        llm=llm,
        tools=registry,
        config=AgentConfig(
            allowed_tools={"get_resolution_time"},
        ),
    )

    with pytest.raises(
        PermissionError,
        match="Tool not allowed: send_email",
    ):
        agent.run(
            system_prompt="You are a business analyst.",
            user_message="Send the report.",
        )