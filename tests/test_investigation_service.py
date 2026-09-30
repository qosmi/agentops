import pandas as pd

from agentops.models import InvestigationRequest
from agentops.services.investigation import InvestigationService


def test_investigation_service_returns_report() -> None:
    tickets = pd.DataFrame(
        [
            {
                "ticket_id": "1",
                "created_at": "2026-08-01T10:00:00",
                "closed_at": "2026-08-01T14:00:00",
                "product": "payments",
                "category": "bug",
                "priority": "high",
            },
            {
                "ticket_id": "2",
                "created_at": "2026-08-02T10:00:00",
                "closed_at": "2026-08-02T18:00:00",
                "product": "payments",
                "category": "bug",
                "priority": "low",
            },
        ]
    )

    service = InvestigationService(
        tickets=tickets,
    )

    report = service.investigate(
        InvestigationRequest(
            question="Why did resolution time increase?",
            requester="test",
        )
    )

    assert report.question == "Why did resolution time increase?"
    assert len(report.findings) == 1
    assert len(report.recommendations) == 1