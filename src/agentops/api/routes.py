from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from agentops.api.dependencies import create_investigation_service
from agentops.api.schemas import (
    HealthResponse,
    InvestigationAPIRequest,
    InvestigationAPIResponse,
)
from agentops.models import InvestigationRequest
from agentops.services.investigation import InvestigationService

router = APIRouter()


InvestigationServiceDependency = Annotated[
    InvestigationService,
    Depends(create_investigation_service),
]


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post(
    "/investigations",
    response_model=InvestigationAPIResponse,
    status_code=status.HTTP_200_OK,
)
def create_investigation(
    request: InvestigationAPIRequest,
    service: InvestigationServiceDependency,
) -> InvestigationAPIResponse:
    try:
        domain_request = InvestigationRequest(
            question=request.question,
            requester="api",
        )
        report = service.investigate(domain_request)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Investigation failed.",
        ) from exc

    return InvestigationAPIResponse(
        investigation_id=str(report.investigation_id),
        question=report.question,
        findings=[
            finding.model_dump()
            for finding in report.findings
        ],
        recommendations=[
            recommendation.model_dump()
            for recommendation in report.recommendations
        ],
    )