from datetime import datetime
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class InvestigationStatus(StrEnum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class InvestigationRequest(BaseModel):
    question: str = Field(min_length=1)
    requester: str = Field(min_length=1)


class Evidence(BaseModel):
    source: str
    claim: str
    value: str
    confidence: float = Field(ge=0.0, le=1.0)


class Finding(BaseModel):
    title: str
    explanation: str
    evidence: list[Evidence]


class Recommendation(BaseModel):
    action: str
    rationale: str
    risk: str


class InvestigationReport(BaseModel):
    investigation_id: UUID
    question: str
    findings: list[Finding]
    recommendations: list[Recommendation]


class Investigation(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    request: InvestigationRequest
    status: InvestigationStatus = InvestigationStatus.PENDING
    created_at: datetime = Field(default_factory=datetime.utcnow)
    report: InvestigationReport | None = None