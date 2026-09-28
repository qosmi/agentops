from collections.abc import Callable
from typing import TypeVar

T = TypeVar("T")


def execute_with_retry[T](
    operation: Callable[[], T],
    max_retries: int,
) -> T:
    attempts = 0

    while True:
        try:
            return operation()
        except Exception:
            attempts += 1

            if attempts > max_retries:
                raise