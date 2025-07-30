from abc import ABC
from dataclasses import dataclass
from typing import Optional

from geometry import Dimension
from grid_entity import GridEntity
from model.portal.door_state import DoorState
from model.portal.portal import Portal


# Added model.occupant.EscapePortal which extends GridEntity class. Added list of walls to the Board. Renamed
# model.occupant.Wall to model.occupant.Vault. The Board has 4 walls so the old name was ambigous and not
# communicating the item's intent."

@dataclass
class Door(GridEntity, Portal, ABC):
    state: DoorState = DoorState.CLOSED

    def __init__(self, id: int, coordinate: Optional[GridCoordinate] = None):
        super().__init__(id=id, dimension=Dimension(1,1), coordinate=coordinate)
        self.state = DoorState.CLOSED


    def open(self):
        if self.state == DoorState.CLOSED:
            self.state = DoorState.OPEN

    def close(self):
        if self.state == DoorState.OPEN:
            self.state = DoorState.CLOSED

    def is_open(self) -> bool:
        return self.state == DoorState.OPEN
