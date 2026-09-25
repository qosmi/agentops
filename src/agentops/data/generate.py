from __future__ import annotations

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path
from uuid import uuid4

from faker import Faker

fake = Faker()

PRODUCTS = [
    "analytics",
    "payments",
    "identity",
    "messaging",
]

CATEGORIES = [
    "bug",
    "billing",
    "configuration",
    "performance",
    "account",
]

PRIORITIES = [
    "low",
    "medium",
    "high",
    "critical",
]


def generate_tickets(
    count: int = 5000,
    seed: int = 42,
) -> list[dict[str, object]]:
    random.seed(seed)
    Faker.seed(seed)

    tickets: list[dict[str, object]] = []

    start = datetime(2026, 7, 1)

    for _ in range(count):
        created_at = start + timedelta(
            minutes=random.randint(0, 60 * 24 * 61)
        )

        product = random.choice(PRODUCTS)
        category = random.choice(CATEGORIES)
        priority = random.choice(PRIORITIES)

        base_hours = {
            "low": 18,
            "medium": 12,
            "high": 8,
            "critical": 3,
        }[priority]

        # Deliberate business pattern:
        # payments tickets became slower in August.
        if product == "payments" and created_at.month == 8:
            base_hours *= 1.8

        noise = random.uniform(0.5, 1.5)
        resolution_hours = base_hours * noise

        closed_at = created_at + timedelta(
            hours=resolution_hours
        )

        tickets.append(
            {
                "ticket_id": str(uuid4()),
                "customer_id": str(uuid4()),
                "created_at": created_at.isoformat(),
                "closed_at": closed_at.isoformat(),
                "product": product,
                "category": category,
                "priority": priority,
            }
        )

    return tickets


def write_csv(
    rows: list[dict[str, object]],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", newline="") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys(),
        )
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    output = Path("data/raw/tickets.csv")

    tickets = generate_tickets()

    write_csv(tickets, output)

    print(f"Wrote {len(tickets)} tickets to {output}")