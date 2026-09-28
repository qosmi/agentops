from pydantic import BaseModel, Field


class AgentConfig(BaseModel):
    max_iterations: int = 5
    allowed_tools: set[str] = Field(default_factory=set)