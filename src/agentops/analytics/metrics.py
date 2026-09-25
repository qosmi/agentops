from datetime import date

from pydantic import BaseModel


class ResolutionMetric(BaseModel):
    period_start: date
    group: str
    ticket_count: int
    average_resolution_hours: float


class TicketVolumeMetric(BaseModel):
    period_start: date
    group: str
    ticket_count: int