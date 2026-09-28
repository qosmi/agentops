from decimal import Decimal

import pandas as pd

from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.models.llm_usage import LLMUsage
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
    registry.register(
        ResolutionTimeTool(tickets)
    )

    return registry


def test_agent_response_can_contain_usage() -> None:
    response = AgentResponse(
        message="Analysis complete.",
        usage=LLMUsage(
            input_tokens=100,
            output_tokens=50,
            total_tokens=150,
            estimated_cost_usd=Decimal("0.001"),
        ),
    )

    assert response.usage.input_tokens == 100
    assert response.usage.output_tokens == 50
    assert response.usage.total_tokens == 150
    assert response.usage.estimated_cost_usd == Decimal("0.001")


def test_agent_loop_accumulates_llm_usage() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need to investigate.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={"group_by": "product"},
                    )
                ],
                usage=LLMUsage(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=150,
                    estimated_cost_usd=Decimal("0.001"),
                ),
            ),
            AgentResponse(
                message="The investigation is complete.",
                usage=LLMUsage(
                    input_tokens=200,
                    output_tokens=100,
                    total_tokens=300,
                    estimated_cost_usd=Decimal("0.002"),
                ),
            ),
        ]
    )

    agent = AgentLoop(
        llm=llm,
        tools=create_registry(),
        config=AgentConfig(
            max_iterations=5,
            allowed_tools={"get_resolution_time"},
        ),
    )

    result = agent.run(
        system_prompt="You are a business analyst.",
        user_message="Why did resolution time increase?",
    )

    assert result == "The investigation is complete."
    assert llm.call_count == 2

    assert llm.responses[0].usage.total_tokens == 150
    assert llm.responses[1].usage.total_tokens == 300