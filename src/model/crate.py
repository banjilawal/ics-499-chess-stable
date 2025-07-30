from dataclasses import dataclass
from typing import Optional

from model.bin import Bin


@dataclass
class Crate(Bin):

    def __init__(self, crate_id: int, coordinate: Optional[GridCoordinate] = None):
        super().__init__(rack_id=crate_id, height=1, coordinate=coordinate)

    def move_left(self, distance: int):
        new_coordinate = GridCoordinate(row=self.coordinate.row, column=self.coordinate.column - distance)
        self.coordinate = new_coordinate

    def move_right(self, distance: int):
        new_coordinate = GridCoordinate(row=self.coordinate.row, column=self.coordinate.column + distance)
        self.coordinate = new_coordinate




    # def mover_id_counter(self) -> int:
    #     return super().mover_id_counter
    #
    # def send_travel_request(self, bearing: Bearing) -> TravelRequest:
    #     pass
    #
    # def accept_travel_decision(self, travel_decision: TravelDecision) -> bool:
    #     pass
    #
    # def move(self, bearing: Bearing) -> bool:
    #     pass

