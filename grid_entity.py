from abc import abstractmethod, ABC
from dataclasses import dataclass, field
from typing import Optional, TYPE_CHECKING

from geometry import Dimension, GridCoordinate

@dataclass
class GridEntity:
    dimension: Dimension
    top_left_coordinate: Optional[GridCoordinate] = None

@dataclass
class BrikPallet(GridEntity):
    pass

@dataclass(kw_only=True)
class Mover(GridEntity, ABC):
    mover_id: int
    movement_strategy: 'MoveStrategy' = field(init=False, repr=False)

    def __init__(self, *, dimension: Dimension, top_left_coordinate: Optional[GridCoordinate] = None, mover_id: int = None):
        if not hasattr(self, 'movement_strategy'):
            raise TypeError(f"{self.__class__.__name__} must initialize movement_strategy")
        super().__init__(dimension=dimension, top_left_coordinate=top_left_coordinate)
        self.mover_id = mover_id

    def move(self, board: 'Board', destination_coordinate: GridCoordinate) -> None:
        if not self.movement_strategy.move(self, board, destination_coordinate):
            print(f"Failed to move {self.mover_id} to {destination_coordinate}.")
        else:
            print(f"Moved {self.mover_id} to {destination_coordinate}.")


@dataclass
class VerticalMover(Mover):
    def __init__(self, *, mover_id: int, length: int, top_left_coordinate: Optional[GridCoordinate] = None):
        self.movement_strategy = VerticalMoveStrategy()
        super().__init__(
            mover_id=mover_id,
            dimension=Dimension(length=length, height=1),
            top_left_coordinate=top_left_coordinate
        )

@dataclass
class HorizontalMover(Mover):
    def __init__(self, *, mover_id: int, height: int, top_left_coordinate: Optional[GridCoordinate] = None):
        self.movement_strategy = HorizontalMoveStrategy()
        super().__init__(
            mover_id=mover_id,
            dimension=Dimension(length=1, height=height),
            top_left_coordinate=top_left_coordinate
         )

@dataclass
class Bishop(Mover):
    def __init__(self, *, mover_id: int,top_left_coordinate: Optional[GridCoordinate] = None):
        self.movement_strategy = BishopMoveStrategy()
        super().__init__(
            mover_id=mover_id,
            dimension=Dimension(length=1, height=1),
            top_left_coordinate=top_left_coordinate
        )

@dataclass
class Knight(Mover):
    def __init__(self, *, mover_id: int,top_left_coordinate: Optional[GridCoordinate] = None):
        self.movement_strategy = KnightMoveStrategy()
        super().__init__(
            mover_id=mover_id,
            dimension=Dimension(length=1, height=1),
            top_left_coordinate=top_left_coordinate
        )

@dataclass
class Castle(Mover):
    def __init__(self, *, mover_id: int, top_left_coordinate: Optional[GridCoordinate] = None):
        self.movement_strategy = CastleMoveStrategy()
        super().__init__(
            mover_id=mover_id,
            dimension=Dimension(length=1, height=1),
            top_left_coordinate=top_left_coordinate
        )

class MoveStrategy(ABC):
    def _check_basic_conditions(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        if mover is None:
            print("[Warning] Mover cannot be None. It cannot move.")
            return False
        if board is None:
            print("[Warning] Board cannot be None. Cannot move.")
            return False
        if mover.top_left_coordinate is None:
            print("[Warning] Mover has no top_left_coordinate. Cannot move.")
            return False
        if destination_coordinate is None:
            print("[Warning] Destination top_left_coordinate cannot be None. Cannot move.")
            return False
        if destination_coordinate.column < 0 or destination_coordinate.column >= board.dimension.length:
            print(f"[Warning] Horizontal move out of bounds: {destination_coordinate.column}")
            return False
        if destination_coordinate.row < 0 or destination_coordinate.row >= board.dimension.length:
            print(f"[Warning] Vertical move out of bounds: {destination_coordinate.row}")
            return False
        return True
    @abstractmethod
    def move(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        pass

class HorizontalMoveStrategy(MoveStrategy):
    def move(self, mover: HorizontalMover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        if destination_coordinate.row != mover.top_left_coordinate.row:
            print("[Warning] Destination top_left_coordinate is not on the same row as the mover. Cannot move.")
            return False

        destination_column = mover.top_left_coordinate.column
        print("strategy calculated destination column:", destination_column)
        return board.move_entity(destination_coordinate, mover) is not None

class VerticalMoveStrategy(MoveStrategy):
    def move(self, mover: VerticalMover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        if destination_coordinate.column != mover.top_left_coordinate.column:
            print("[Warning] Destination top_left_coordinate is not on the same column as the mover. Cannot move.")
            return False

        destination_row = mover.top_left_coordinate.row
        print("strategy calculated destination row:", destination_row)
        return board.move_entity(destination_coordinate, mover) is not None


class KnightMoveStrategy(MoveStrategy):
    def move(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        current_pos = mover.top_left_coordinate

        # Calculate the differences
        row_diff = abs(destination_coordinate.row - current_pos.row)
        col_diff = abs(destination_coordinate.column - current_pos.column)

        # Knight moves in L-shape: (2,1) or (1,2)
        is_valid_knight_move = (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)

        if not is_valid_knight_move:
            print(f"[Warning] Knight can only move in L-shape (2+1 or 1+2). Current move: {row_diff}+{col_diff}")
            return False

        print(f"[Info] Valid knight move from {current_pos} to {destination_coordinate}")
        return board.move_entity(destination_coordinate, mover) is not None



class CastleMoveStrategy(MoveStrategy):
    def move(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        print(f"[DEBUG] Castle move attempt from {mover.top_left_coordinate} to {destination_coordinate}")

        # Castle can move horizontally or vertically
        is_horizontal = destination_coordinate.row == mover.top_left_coordinate.row
        is_vertical = destination_coordinate.column == mover.top_left_coordinate.column

        print(f"[DEBUG] Is horizontal: {is_horizontal}, Is vertical: {is_vertical}")

        if is_horizontal or is_vertical:
            result = board.move_entity(destination_coordinate, mover) is not None
            print(f"[DEBUG] Move result: {result}")
            return result

        print("[DEBUG] Move rejected - not horizontal or vertical")
        return False

class BishopMoveStrategy(MoveStrategy):
    def move(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        if not self._check_basic_conditions(mover, board, destination_coordinate):
            return False

        origin = mover.top_left_coordinate
        row_diff = abs(destination_coordinate.row - origin.row)
        col_diff = abs(destination_coordinate.column - origin.column)

        if row_diff != col_diff:
            print("[Warning] Diagonal move must have equal row and column delta.")
            return False

        print(f"[Info] Diagonal move approved from {origin} to {destination_coordinate}.")
        return board.move_entity(destination_coordinate, mover) is not None

class DragStrategy(ABC):
    def move(self, mover: Mover, board: 'Board', destination_coordinate: GridCoordinate) -> bool:
        pass