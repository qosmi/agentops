from typing import Any

import pandas as pd

from agentops.analytics.resolution_time import (
    calculate_resolution_time,
)
from agentops.tools.base import Tool


class ResolutionTimeTool(Tool):
    name = "get_resolution_time"

    description = (
        "Calculate average ticket resolution time grouped "
        "by product, category, or priority."
    )

    def __init__(self, tickets: pd.DataFrame) -> None:
        self.tickets = tickets

    def execute(
        self,
        arguments: dict[str, Any],
    ) -> Any:
        group_by = arguments.get("group_by")

        if not isinstance(group_by, str):
            raise ValueError(
                "group_by must be a string"
            )

        return calculate_resolution_time(
            self.tickets,
            group_by,
        )