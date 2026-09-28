from enum import StrEnum


class InvestigationState(StrEnum):
    CREATED = "created"
    PLANNING = "planning"
    INVESTIGATING = "investigating"
    VERIFYING = "verifying"
    COMPLETED = "completed"
    FAILED = "failed"