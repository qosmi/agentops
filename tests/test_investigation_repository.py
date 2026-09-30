from uuid import uuid4

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from agentops.db.base import Base
from agentops.db.models import InvestigationRecord
from agentops.models import (
    Evidence,
    Finding,
    InvestigationReport,
    InvestigationRequest,
    Recommendation,
)
from agentops.repositories.investigation import InvestigationRepository


def create_session() -> Session:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(engine)

    return Session(engine)


def create_report() -> InvestigationReport:
    return InvestigationReport(
        investigation_id=uuid4(),
        question="Why did resolution time increase?",
        findings=[
            Finding(
                title="Payments resolution time increased",
                explanation=(
                    "Payments tickets show elevated "
                    "resolution time during August."
                ),
                evidence=[
                    Evidence(
                        source="ticket_data",
                        claim=(
                            "Payments tickets had elevated "
                            "resolution time in August."
                        ),
                        value="6.00 hours",
                        confidence=0.95,
                    )
                ],
            )
        ],
        recommendations=[
            Recommendation(
                action="Investigate the August payments workload",
                rationale=(
                    "The data indicates that payments tickets "
                    "experienced elevated resolution time."
                ),
                risk="low",
            )
        ],
    )


def test_repository_saves_investigation() -> None:
    session = create_session()

    try:
        repository = InvestigationRepository(session)

        request = InvestigationRequest(
            question="Why did resolution time increase?",
            requester="test",
        )

        report = create_report()

        record = repository.save(
            request=request,
            report=report,
        )

        assert record.investigation_id == str(
            report.investigation_id
        )
        assert record.question == request.question
        assert record.requester == "test"
        assert record.report["question"] == request.question
    finally:
        session.close()


def test_repository_gets_investigation() -> None:
    session = create_session()

    try:
        repository = InvestigationRepository(session)

        request = InvestigationRequest(
            question="Why did resolution time increase?",
            requester="test",
        )

        report = create_report()

        repository.save(
            request=request,
            report=report,
        )

        result = repository.get(
            report.investigation_id
        )

        assert result is not None
        assert result.investigation_id == str(
            report.investigation_id
        )
        assert result.question == request.question
        assert result.report["question"] == request.question
    finally:
        session.close()


def test_repository_returns_none_for_unknown_investigation() -> None:
    session = create_session()

    try:
        repository = InvestigationRepository(session)

        result = repository.get(uuid4())

        assert result is None
    finally:
        session.close()


def test_database_model_is_registered() -> None:
    assert InvestigationRecord.__tablename__ == "investigations"
    assert "investigations" in Base.metadata.tables