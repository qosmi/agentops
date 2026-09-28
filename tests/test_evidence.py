from agentops.models.evidence import Evidence


def test_evidence_stores_source_and_value() -> None:
    evidence = Evidence(
        source="get_resolution_time",
        value={
            "payments": 6.0,
            "billing": 3.0,
        },
    )

    assert evidence.source == "get_resolution_time"
    assert evidence.value == {
        "payments": 6.0,
        "billing": 3.0,
    }