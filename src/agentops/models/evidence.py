from typing import Any

from pydantic import BaseModel


class Evidence(BaseModel):
    source: str
    value: Any