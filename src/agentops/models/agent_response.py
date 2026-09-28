from pydantic import BaseModel, Field

from agentops.models.tool_call import ToolCall


class AgentResponse(BaseModel):
    message: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)