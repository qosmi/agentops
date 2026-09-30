from pathlib import Path

import pandas as pd

from agentops.services.investigation import InvestigationService

DATA_PATH = Path("data/raw/tickets.csv")


def create_investigation_service() -> InvestigationService:
    if not DATA_PATH.exists():
        raise RuntimeError(
            f"Required dataset does not exist: {DATA_PATH}"
        )

    tickets = pd.read_csv(DATA_PATH)

    return InvestigationService(
        tickets=tickets,
    )