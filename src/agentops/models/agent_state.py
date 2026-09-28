from pydantic import BaseModel, Field


class AgentState(BaseModel):
    system_prompt: str
    messages: list[dict[str, str]] = Field(default_factory=list)
    iteration: int = 0
    final_answer: str | None = None