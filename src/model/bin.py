from dataclasses import dataclass
from typing import Optional

from geometry import Dimension
from grid_entity import GridEntity


@dataclass
class Bin(GridEntity):

    def __init__(self, rack_id: int, height: int, coordinate: Optional[GridCoordinate] = None):
        super().__init__(id=rack_id, dimension=Dimension(length=1, height=height), coordinate=coordinate)

    def move_up(self, distance: int):
        new_coordinate = GridCoordinate(row=self.coordinate.row - distance, column=self.coordinate.column)
        self.coordinate = new_coordinate

    def move_down(self, distance: int):
        new_coordinate = GridCoordinate(row=self.coordinate.row + distance, column=self.coordinate.column)
        self.coordinate = new_coordinate

    def print_info(self) -> None:
        if self.coordinate:
            print(f"Bin {self.id} at position (row: {self.coordinate.row}, column: {self.coordinate.column})")
        else:
            print(f"Bin {self.id} - not placed")
        print("Bin area:", self.dimension.area())
