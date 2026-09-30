import pandas as pd
from fastapi.testclient import TestClient

from agentops.api.dependencies import create_investigation_service
from agentops.api.main import app
from agentops.services.investigation import InvestigationService


def create_test_service() -> InvestigationService:
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

    return InvestigationService(
        tickets=tickets,
    )


def test_health_endpoint() -> None:
    app.dependency_overrides[
        create_investigation_service
    ] = create_test_service

    try:
        client = TestClient(app)

        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "status": "ok",
        }
    finally:
        app.dependency_overrides.clear()


def test_create_investigation() -> None:
    app.dependency_overrides[
        create_investigation_service
    ] = create_test_service

    try:
        client = TestClient(app)

        response = client.post(
            "/investigations",
            json={
                "question": (
                    "Why did resolution time increase?"
                ),
            },
        )

        assert response.status_code == 200

        body = response.json()

        assert body["question"] == (
            "Why did resolution time increase?"
        )

        assert len(body["findings"]) == 1
        assert body["findings"][0]["title"] == (
            "Payments resolution time increased"
        )

        assert len(body["recommendations"]) == 1
        assert body["recommendations"][0]["risk"] == (
            "low"
        )

        assert body["investigation_id"]
    finally:
        app.dependency_overrides.clear()


def test_create_investigation_rejects_empty_question() -> None:
    app.dependency_overrides[
        create_investigation_service
    ] = create_test_service

    try:
        client = TestClient(app)

        response = client.post(
            "/investigations",
            json={
                "question": "",
            },
        )

        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()


def test_create_investigation_rejects_missing_question() -> None:
    app.dependency_overrides[
        create_investigation_service
    ] = create_test_service

    try:
        client = TestClient(app)

        response = client.post(
            "/investigations",
            json={},
        )

        assert response.status_code == 422
    finally:
        app.dependency_overrides.clear()