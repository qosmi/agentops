import logging

from agentops.observability.events import AgentEvent
from agentops.observability.logger import AgentLogger


class RecordingLogger:
    def __init__(self) -> None:
        self.events: list[AgentEvent] = []

    def log(self, event: AgentEvent) -> None:
        self.events.append(event)


def test_agent_event_contains_timestamp() -> None:
    event = AgentEvent(
        event_type="agent_started",
        iteration=0,
    )

    assert event.event_type == "agent_started"
    assert event.iteration == 0
    assert event.timestamp.tzinfo is not None


def test_agent_event_stores_data() -> None:
    event = AgentEvent(
        event_type="tool_started",
        iteration=1,
        data={
            "tool_name": "get_resolution_time",
        },
    )

    assert event.data["tool_name"] == (
        "get_resolution_time"
    )


def test_agent_logger_writes_structured_json(
    caplog: object,
) -> None:
    logger = logging.getLogger(
        "agentops.test.observability"
    )

    agent_logger = AgentLogger(
        logger=logger,
    )

    event = AgentEvent(
        event_type="agent_started",
        iteration=0,
        data={
            "user_message": "Investigate resolution time",
        },
    )

    with caplog.at_level(
        logging.INFO,
        logger="agentops.test.observability",
    ):
        agent_logger.log(event)

    assert len(caplog.records) == 1
    assert '"event_type": "agent_started"' in (
        caplog.records[0].message
    )
    assert (
        '"iteration": 0'
        in caplog.records[0].message
    )