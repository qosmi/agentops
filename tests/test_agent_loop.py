import pandas as pd

from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_response import AgentResponse
from agentops.models.tool_call import ToolCall
from agentops.tools.registry import ToolRegistry
from agentops.tools.resolution_time import ResolutionTimeTool


def test_agent_loop_calls_tool_then_finishes() -> None:
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

    registry.register(
        ResolutionTimeTool(tickets)
    )

    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need to inspect resolution time.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={
                            "group_by": "product"
                        },
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
        user_message=(
            "Why did resolution time increase?"
        ),
    )

    assert "6 hours" in result
    assert llm.call_count == 2


def test_agent_loop_updates_conversation_between_iterations() -> None:
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
        ]
    )

    registry = ToolRegistry()
    registry.register(ResolutionTimeTool(tickets))

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
            AgentResponse(
                message="The investigation is complete."
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

    assert result == "The investigation is complete."
    assert llm.call_count == 2