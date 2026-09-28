import pandas as pd
import pytest

from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
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


def test_agent_loop_calls_tool_then_finishes() -> None:
    registry = create_registry()

    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need to inspect resolution time.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={"group_by": "product"},
                    )
                ],
            ),
            AgentResponse(
                message=(
                    "The payments product has an "
                    "average resolution time of 6 hours."
                ),
            ),
        ]
    )

    agent = AgentLoop(
        llm=llm,
        tools=registry,
    )

    result = agent.run(
        system_prompt="You are a business analyst.",
        user_message="Why did resolution time increase?",
    )

    assert "6 hours" in result
    assert llm.call_count == 2


def test_agent_loop_stops_after_max_iterations() -> None:
    registry = create_registry()

    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need more data.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={"group_by": "product"},
                    )
                ],
            ),
            AgentResponse(
                message="I still need more data.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={"group_by": "product"},
                    )
                ],
            ),
        ]
    )

    agent = AgentLoop(
        llm=llm,
        tools=registry,
        max_iterations=2,
    )

    with pytest.raises(
        RuntimeError,
        match="maximum iterations: 2",
    ):
        agent.run(
            system_prompt="You are a business analyst.",
            user_message="Investigate the problem.",
        )

    assert llm.call_count == 2


def test_agent_loop_rejects_invalid_max_iterations() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="Done.",
            ),
        ]
    )

    registry = ToolRegistry()

    with pytest.raises(
        ValueError,
        match="max_iterations must be at least 1",
    ):
        AgentLoop(
            llm=llm,
            tools=registry,
            max_iterations=0,
        )