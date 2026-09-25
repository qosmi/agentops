from __future__ import annotations

import pandas as pd

from agentops.analytics.metrics import ResolutionMetric


def calculate_resolution_time(
    tickets: pd.DataFrame,
    group_by: str,
) -> list[ResolutionMetric]:
    allowed_groups = {
        "product",
        "category",
        "priority",
    }

    if group_by not in allowed_groups:
        raise ValueError(
            f"Unsupported group_by: {group_by}"
        )

    data = tickets.copy()

    data["created_at"] = pd.to_datetime(
        data["created_at"]
    )
    data["closed_at"] = pd.to_datetime(
        data["closed_at"]
    )

    data["resolution_hours"] = (
        data["closed_at"] - data["created_at"]
    ).dt.total_seconds() / 3600

    data["period_start"] = (
        data["created_at"]
        .dt.to_period("M")
        .dt.to_timestamp()
        .dt.date
    )

    grouped = (
        data.groupby(
            ["period_start", group_by],
            as_index=False,
        )
        .agg(
            ticket_count=("ticket_id", "count"),
            average_resolution_hours=(
                "resolution_hours",
                "mean",
            ),
        )
    )

    return [
        ResolutionMetric(
            period_start=row["period_start"],
            group=row[group_by],
            ticket_count=int(row["ticket_count"]),
            average_resolution_hours=float(
                row["average_resolution_hours"]
            ),
        )
        for _, row in grouped.iterrows()
    ]