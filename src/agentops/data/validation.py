import pandas as pd
import pandera.pandas as pa


ticket_schema = pa.DataFrameSchema(
    {
        "ticket_id": pa.Column(str, unique=True),
        "customer_id": pa.Column(str),
        "created_at": pa.Column(str),
        "closed_at": pa.Column(str),
        "product": pa.Column(
            str,
            checks=pa.Check.isin(
                [
                    "analytics",
                    "payments",
                    "identity",
                    "messaging",
                ]
            ),
        ),
        "category": pa.Column(
            str,
            checks=pa.Check.isin(
                [
                    "bug",
                    "billing",
                    "configuration",
                    "performance",
                    "account",
                ]
            ),
        ),
        "priority": pa.Column(
            str,
            checks=pa.Check.isin(
                [
                    "low",
                    "medium",
                    "high",
                    "critical",
                ]
            ),
        ),
    }
)


def validate_tickets(df: pd.DataFrame) -> pd.DataFrame:
    validated = ticket_schema.validate(df)

    created = pd.to_datetime(validated["created_at"])
    closed = pd.to_datetime(validated["closed_at"])

    if not (created <= closed).all():
        raise ValueError(
            "Found tickets where closed_at occurs before created_at"
        )

    return validated