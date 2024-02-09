"""Contains basic Mocks classes"""

from dataclasses import dataclass
from typing import Any


@dataclass
class MockedListResult:
    data: list[Any]

    def all(self) -> list[Any]:
        return self.data
