from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4

@dataclass(frozen=True)
class GridCoordinate:
    row: int
    column: int

    def __post_init__(self):
        if self.row < 0:
            raise ValueError("Row cannot be negative")
        if self.column < 0:
            raise ValueError("Column cannot be negative")

@dataclass(frozen=True)
class Dimension:

    MIN_LENGTH = 1
    MIN_HEIGHT = 1
    MIN_AREA = MIN_LENGTH * MIN_HEIGHT

    length: int
    height: int

    def __post_init__(self):
        if self.length < 1:
            raise ValueError("length must be greater than 0")
        if self.height < 1:
            raise ValueError("height must be greater than 0")

    def area(self) -> int:
        return self.length * self.height