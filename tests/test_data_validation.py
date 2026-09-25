import pandas as pd
import pytest

from agentops.data.validation import validate_tickets


def test_valid_ticket() -> None:
    df = pd.DataFrame(
        [
            {
                "ticket_id": "1",
                "customer_id": "customer-1",
                "created_at": "2026-08-01T10:00:00",
                "closed_at": "2026-08-01T12:00:00",
                "product": "payments",
                "category": "bug",
                "priority": "high",
            }
        ]
    )

    result = validate_tickets(df)

    assert len(result) == 1


def test_invalid_product_is_rejected() -> None:
    df = pd.DataFrame(
        [
            {
                "ticket_id": "1",
                "customer_id": "customer-1",
                "created_at": "2026-08-01T10:00:00",
                "closed_at": "2026-08-01T12:00:00",
                "product": "unknown",
                "category": "bug",
                "priority": "high",
            }
        ]
    )

    with pytest.raises(Exception):
        validate_tickets(df)