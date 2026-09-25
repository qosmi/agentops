import pandas as pd

from agentops.analytics.resolution_time import (
    calculate_resolution_time,
)


def test_resolution_time_is_calculated() -> None:
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

    result = calculate_resolution_time(
        tickets,
        group_by="product",
    )

    assert len(result) == 1
    assert result[0].group == "payments"
    assert result[0].ticket_count == 2
    assert result[0].average_resolution_hours == 6.0