from pydantic import BaseModel, Field

from agentops.models.agent_observation import AgentObservation
from agentops.models.evidence import Evidence
from agentops.models.investigation_state import InvestigationState


class AgentState(BaseModel):
    system_prompt: str
    messages: list[dict[str, str]] = Field(default_factory=list)
    iteration: int = 0
    final_answer: str | None = None
    observations: list[AgentObservation] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    investigation_state: InvestigationState = InvestigationState.CREATED