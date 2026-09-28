import json
import logging

from agentops.observability.events import AgentEvent


class AgentLogger:
    def __init__(
        self,
        logger: logging.Logger | None = None,
    ) -> None:
        self.logger = logger or logging.getLogger(
            "agentops.agent"
        )

    def log(self, event: AgentEvent) -> None:
        self.logger.info(
            json.dumps(
                event.model_dump(mode="json"),
                sort_keys=True,
            )
        )