from pydantic import BaseModel

from agentops.models.tool_call import ToolCall


class AgentResponse(BaseModel):
    message: str
    tool_calls: list[ToolCall] = []