from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    name: str
    description: str

    @abstractmethod
    def execute(self, arguments: dict[str, Any]) -> Any:
        raise NotImplementedError