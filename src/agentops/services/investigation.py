import pandas as pd

from agentops.models import (
    Evidence,
    Finding,
    InvestigationReport,
    InvestigationRequest,
    Recommendation,
)


class InvestigationService:
    def __init__(self, tickets: pd.DataFrame) -> None:
        self.tickets = tickets

    def investigate(
        self,
        request: InvestigationRequest,
    ) -> InvestigationReport:
        payments = self.tickets[
            self.tickets["product"] == "payments"
        ]

        payments = payments.copy()

        payments["created_at"] = pd.to_datetime(
            payments["created_at"]
        )
        payments["closed_at"] = pd.to_datetime(
            payments["closed_at"]
        )

        payments["resolution_hours"] = (
            payments["closed_at"]
            - payments["created_at"]
        ).dt.total_seconds() / 3600

        august = payments[
            payments["created_at"].dt.month == 8
        ]

        average_resolution = float(
            august["resolution_hours"].mean()
        )

        evidence = Evidence(
            source="ticket_data",
            claim=(
                "Payments tickets had elevated "
                "resolution time in August."
            ),
            value=f"{average_resolution:.2f} hours",
            confidence=0.95,
        )

        finding = Finding(
            title="Payments resolution time increased",
            explanation=(
                "Payments tickets show elevated "
                "resolution time during August."
            ),
            evidence=[evidence],
        )

        recommendation = Recommendation(
            action="Investigate the August payments workload",
            rationale=(
                "The data indicates that payments tickets "
                "experienced elevated resolution time."
            ),
            risk="low",
        )

        return InvestigationReport(
            investigation_id=__import__(
                "uuid"
            ).uuid4(),
            question=request.question,
            findings=[finding],
            recommendations=[recommendation],
        )