from pydantic import BaseModel, Field


class InvestigationAPIRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=4000,
    )


class InvestigationAPIResponse(BaseModel):
    investigation_id: str
    question: str
    findings: list[dict[str, object]]
    recommendations: list[dict[str, object]]


class HealthResponse(BaseModel):
    status: str