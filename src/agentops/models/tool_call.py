from typing import Any

from pydantic import BaseModel


class ToolCall(BaseModel):
    tool_name: str
    arguments: dict[str, Any]