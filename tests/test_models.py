from agentops.models import (
    Evidence,
    Finding,
    Investigation,
    InvestigationRequest,
    InvestigationStatus,
)


def test_investigation_has_id() -> None:
    investigation = Investigation(
        request=InvestigationRequest(
            question="Why did resolution time increase?",
            requester="demo-user",
        )
    )

    assert investigation.id is not None
    assert investigation.status == InvestigationStatus.PENDING


def test_evidence_confidence_must_be_between_zero_and_one() -> None:
    evidence = Evidence(
        source="sql:resolution_time",
        claim="Resolution time increased",
        value="31%",
        confidence=0.91,
    )

    assert evidence.confidence == 0.91


def test_finding_contains_evidence() -> None:
    evidence = Evidence(
        source="sql:resolution_time",
        claim="Resolution time increased",
        value="31%",
        confidence=0.91,
    )

    finding = Finding(
        title="Resolution time increased",
        explanation="Average resolution time increased by 31%.",
        evidence=[evidence],
    )

    assert len(finding.evidence) == 1