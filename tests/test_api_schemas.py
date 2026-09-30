import pytest
from pydantic import ValidationError

from agentops.api.schemas import InvestigationAPIRequest


def test_investigation_api_request_accepts_question() -> None:
    request = InvestigationAPIRequest(
        question="Why did resolution time increase?"
    )

    assert request.question == (
        "Why did resolution time increase?"
    )


def test_investigation_api_request_rejects_empty_question() -> None:
    with pytest.raises(ValidationError):
        InvestigationAPIRequest(
            question=""
        )


def test_investigation_api_request_rejects_missing_question() -> None:
    with pytest.raises(ValidationError):
        InvestigationAPIRequest.model_validate({})