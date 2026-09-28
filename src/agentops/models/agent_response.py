from pydantic import BaseModel, Field

from agentops.models.llm_usage import LLMUsage
from agentops.models.tool_call import ToolCall


class AgentResponse(BaseModel):
    message: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    usage: LLMUsage = Field(default_factory=LLMUsage)