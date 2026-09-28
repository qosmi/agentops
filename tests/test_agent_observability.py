import pandas as pd

from agentops.agents.loop import AgentLoop
from agentops.llm.fake import FakeLLMProvider
from agentops.models.agent_config import AgentConfig
from agentops.models.agent_response import AgentResponse
from agentops.models.llm_usage import LLMUsage
from agentops.models.tool_call import ToolCall
from agentops.observability.events import AgentEvent
from agentops.tools.registry import ToolRegistry
from agentops.tools.resolution_time import ResolutionTimeTool


class RecordingLogger:
    def __init__(self) -> None:
        self.events: list[AgentEvent] = []

    def log(self, event: AgentEvent) -> None:
        self.events.append(event)


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


def test_agent_loop_records_execution_events() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need to investigate.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={
                            "group_by": "product"
                        },
                    )
                ],
                usage=LLMUsage(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=150,
                ),
            ),
            AgentResponse(
                message="The investigation is complete.",
                usage=LLMUsage(
                    input_tokens=200,
                    output_tokens=100,
                    total_tokens=300,
                ),
            ),
        ]
    )

    recording_logger = RecordingLogger()

    agent = AgentLoop(
        llm=llm,
        tools=create_registry(),
        config=AgentConfig(
            max_iterations=5,
            allowed_tools={
                "get_resolution_time"
            },
        ),
        logger=recording_logger,
    )

    result = agent.run(
        system_prompt="You are a business analyst.",
        user_message="Why did resolution time increase?",
    )

    assert result == "The investigation is complete."

    event_types = [
        event.event_type
        for event in recording_logger.events
    ]

    assert event_types == [
        "agent_started",
        "llm_request",
        "llm_response",
        "tool_started",
        "tool_completed",
        "llm_request",
        "llm_response",
        "agent_completed",
    ]


def test_agent_loop_records_token_usage() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="Done.",
                usage=LLMUsage(
                    input_tokens=100,
                    output_tokens=50,
                    total_tokens=150,
                ),
            ),
        ]
    )

    recording_logger = RecordingLogger()

    agent = AgentLoop(
        llm=llm,
        tools=ToolRegistry(),
        config=AgentConfig(
            max_iterations=5,
            allowed_tools=set(),
        ),
        logger=recording_logger,
    )

    result = agent.run(
        system_prompt="You are a business analyst.",
        user_message="Investigate the issue.",
    )

    assert result == "Done."

    response_event = next(
        event
        for event in recording_logger.events
        if event.event_type == "llm_response"
    )

    assert response_event.data["input_tokens"] == 100
    assert response_event.data["output_tokens"] == 50
    assert response_event.data["total_tokens"] == 150


def test_agent_loop_records_tool_denial() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need the resolution data.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={
                            "group_by": "product"
                        },
                    )
                ],
            ),
        ]
    )

    recording_logger = RecordingLogger()

    agent = AgentLoop(
        llm=llm,
        tools=create_registry(),
        config=AgentConfig(
            max_iterations=5,
            allowed_tools=set(),
        ),
        logger=recording_logger,
    )

    try:
        agent.run(
            system_prompt="You are a business analyst.",
            user_message="Investigate the issue.",
        )
    except PermissionError:
        pass

    event_types = [
        event.event_type
        for event in recording_logger.events
    ]

    assert "tool_denied" in event_types
    assert "agent_completed" not in event_types


def test_agent_loop_records_max_iteration_failure() -> None:
    llm = FakeLLMProvider(
        responses=[
            AgentResponse(
                message="I need more information.",
                tool_calls=[
                    ToolCall(
                        tool_name="get_resolution_time",
                        arguments={
                            "group_by": "product"
                        },
                    )
                ],
            ),
        ]
    )

    recording_logger = RecordingLogger()

    agent = AgentLoop(
        llm=llm,
        tools=create_registry(),
        config=AgentConfig(
            max_iterations=1,
            allowed_tools={
                "get_resolution_time"
            },
        ),
        logger=recording_logger,
    )

    try:
        agent.run(
            system_prompt="You are a business analyst.",
            user_message="Investigate the issue.",
        )
    except RuntimeError:
        pass

    event_types = [
        event.event_type
        for event in recording_logger.events
    ]

    assert event_types[-1] == "agent_failed"