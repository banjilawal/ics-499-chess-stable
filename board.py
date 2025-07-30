import random
from dataclasses import dataclass, field

from typing import Tuple, List, Optional, cast

from exception import InvalidIdError
from geometry import Dimension, GridCoordinate
from grid_entity import GridEntity, Mover

from constants import Config
from id_factory import id_factory

@dataclass
class Cell:
    id: int
    coordinate: GridCoordinate
    occupant: Optional['GridEntity'] = field(default=None)

    def __post_init__(self):
        object.__setattr__(self, 'mover_id_counter', self.id)
        object.__setattr__(self, 'top_left_coordinate', self.coordinate)
        object.__setattr__(self, 'occupant', self.occupant)

@dataclass
class Board:
    MIN_ROW_COUNT = 6
    MIN_COLUMN_COUNT = 6

    entities: List[GridEntity] = field(default_factory=list)

    cells: Tuple[Tuple[Cell, ...], ...] = field(init=False, repr=False)
    dimension: Dimension = field(
        default_factory=lambda: Dimension(length=Config.COLUMN_COUNT, height=Config.ROW_COUNT))

    def __post_init__(self):
        if not all([
            self.dimension.height > self.MIN_ROW_COUNT,
            self.dimension.length > self.MIN_COLUMN_COUNT
        ]):
            raise ValueError("Board dimensions below minimum values")

        cells = tuple(
            tuple(
                Cell(
                    id=id_factory.cell_id(),
                    coordinate=GridCoordinate(row=row, column=col)
                )
                for col in range(self.dimension.length)
            )
            for row in range(self.dimension.height)
        )
        object.__setattr__(self, 'cells', cells)

    def get_mover_by_id(self, mover_id: int) -> Optional[GridEntity]:
        for entity in self.entities:
            print(entity)
            if entity.id == mover_id:
                return entity
        return None

    def get_all_movers(self) -> List[Mover]:
        movers = []
        for entity in self.entities:
            if isinstance(entity, Mover):
                mover = cast(Mover, entity)
                if mover not in movers:
                    movers.append(mover)
        return self.entities

    def get_empty_cells(self) -> List[Cell]:
        empty_cells = []
        for row in self.cells:
            for cell in row:
                if cell.occupant is None and cell not in empty_cells:
                    empty_cells.append(cell)
        return empty_cells

    def get_occupied_cells(self) -> List[Cell]:
        occupied_cells = []
        for row in self.cells:
            for cell in row:
                if cell.occupant is not None and cell not in occupied_cells:
                    occupied_cells.append(cell)
        return occupied_cells

    def get_cells_by_area(self, top_left_coordinate: GridCoordinate, dimension: Dimension) -> List[Cell]:
        if top_left_coordinate is None or dimension is None:
            raise ValueError("Coordinate and dimension must not be None.")

        start_row = top_left_coordinate.row
        start_col = top_left_coordinate.column

        end_row = start_row + dimension.height - 1
        end_col = start_col + dimension.length - 1

        cells_in_area = []
        for r in range(start_row, end_row + 1):
            for c in range(start_col, end_col + 1):
                cells_in_area.append(self.cells[r][c])
        return cells_in_area

    def get_cells_occupied_by_entity(self, entity: GridEntity) -> List[Cell]:
        if entity is None:
            return []
        occupied_cells = []
        for row in self.cells:
            for cell in row:
                if cell.occupant == entity:
                    occupied_cells.append(cell)
        return occupied_cells

    def remove_entity_from_cells(self, mover: Mover) -> None:
        if mover is None:
            raise ValueError("Entity not found on the board. cannot remove a non-existent mover.")

        target_cells = self.get_cells_occupied_by_entity(mover)
        for cell in target_cells:
            if cell.occupant == mover:
                cell.occupant = None

    def add_entity_to_area(self, entity: GridEntity, top_left_coordinate: GridCoordinate) -> None:

        if top_left_coordinate is None:
            raise ValueError("Cannot add mover to an area without a top-left top_left_coordinate.")

        if entity is None:
            raise ValueError("Entity not found on the board. cannot add a non-existent mover.")

        if entity is None or top_left_coordinate is None:
            raise ValueError("Entity and top_left_coordinate must not be None.")

        target_cells = self.get_cells_by_area(top_left_coordinate, entity.dimension)

        for cell in target_cells:
            cell.occupant = entity
        entity.top_left_coordinate = top_left_coordinate

    def add_new_entity(self, top_left_coordinate: GridCoordinate, entity: GridEntity) -> Optional[GridEntity]:
        if top_left_coordinate is None or entity is None:
            raise ValueError("Top-left top_left_coordinate and mover must not be None.")

        # Bounds check
        if top_left_coordinate.row + entity.dimension.height > self.dimension.height:
            raise Exception("Entity does not fit within board bounds at the specified top_left_coordinate.")

        if top_left_coordinate.column + entity.dimension.length > self.dimension.length:
            raise Exception("Entity does not fit within board bounds at the specified top_left_coordinate.")

        if not self.can_entity_move_to_cells(entity, top_left_coordinate):
            print("Coordinate", top_left_coordinate, "is ouccupoied by another entity. Canni=ot move here")
            return None

        self.register_new_entity(entity)
        self.add_entity_to_area(entity, top_left_coordinate)
        return entity

    def move_entity(self, upper_left_destination: GridCoordinate, mover: Mover) -> Optional[Mover]:
        if upper_left_destination is None:
            raise ValueError("Destination top_left_coordinate must not be None.")

        if mover is None:
            raise ValueError("Entity does not exist. in the board. cannot move a non-existent mover.")

        if not self.can_entity_move_to_cells(mover, upper_left_destination):
            print("Entity", mover.mover_id, "cannot move to", upper_left_destination)
            return None

        self.remove_entity_from_cells(mover)
        self.add_entity_to_area(mover, upper_left_destination)
        return mover

    def remove_entity(self, entity: GridEntity) -> None:
        if entity is None:
            raise ValueError("Entity does not exist. in the board. cannot remove a non-existent mover.")
        self.remove_entity_from_cells(entity)
        self.entities.remove(entity)

    def can_entity_move_to_cells(self, entity: GridEntity, new_top_left_coordinate: GridCoordinate) -> bool:
        if entity is None or new_top_left_coordinate is None:
            raise ValueError("Entity and coordinate must not be None.")

        if (new_top_left_coordinate.row < 0 or new_top_left_coordinate.column < 0 or
                new_top_left_coordinate.row + entity.dimension.height > self.dimension.height or
                new_top_left_coordinate.column + entity.dimension.length > self.dimension.length):
            return False

        entity_height = entity.dimension.height
        entity_length = entity.dimension.length

        # Top-left (already have this as new_top_left_coordinate)
        top = new_top_left_coordinate.row
        left = new_top_left_coordinate.column

        # Bottom-right
        bottom = top + entity_height - 1
        right = left + entity_length - 1

        # Boundary checks (all must be True)
        if not (0 <= top < self.dimension.height and
                0 <= left < self.dimension.length and
                0 <= bottom < self.dimension.height and
                0 <= right < self.dimension.length):
            return False

        # Collision detection (now using proper boundaries)
        for r in range(top, bottom + 1):
            for c in range(left, right + 1):
                cell = self.cells[r][c]
                if cell.occupant is not None and cell.occupant != entity:
                    return False
        return True

    def random_empty_cell(self) -> Optional[Cell]:
        if len(self.get_empty_cells()) == 0:
            return None
        cell = random.choice(self.get_empty_cells())
        while cell is None:
            cell = random.choice(self.get_empty_cells())
        return cell

    def register_new_entity(self, entity: GridEntity) -> None:
        if entity is None:
            raise ValueError("Entity must not be None.")

        if entity not in self.entities:
            self.entities.append(entity)
