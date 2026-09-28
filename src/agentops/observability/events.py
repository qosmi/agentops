from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class AgentEvent(BaseModel):
    event_type: str
    timestamp: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    iteration: int
    data: dict[str, Any] = Field(default_factory=dict)