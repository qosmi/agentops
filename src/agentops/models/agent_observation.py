from typing import Any

from pydantic import BaseModel


class AgentObservation(BaseModel):
    iteration: int
    tool_name: str
    arguments: dict[str, Any]
    result: Any