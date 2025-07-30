import random
from typing import List

from board import Board
from grid_entity import HorizontalMover, VerticalMover
from geometry import Dimension
from id_factory import id_factory


class EntityFactory:

    @staticmethod
    def build_dimension(max_length: int, max_height: int) -> Dimension:
        return Dimension(
            length=random.randint(1, max_length),
            height=random.randint(1, max_height)
        )

    @staticmethod
    def build_horizontal_mover(max_height: int) -> HorizontalMover:
        mover = HorizontalMover(
            mover_id=id_factory.mover_id(),
            height=random.randint(1, max_height),
            top_left_coordinate=None
        )
        print(mover)
        return mover

    @staticmethod
    def build_horizontal_mover_list(max_height: int, count: int) -> List[HorizontalMover]:
        return [EntityFactory.build_horizontal_mover(max_height) for _ in range(count)]

    @staticmethod
    def build_vertical_mover(max_length: int) -> HorizontalMover:
        mover = VerticalMover(
            mover_id=id_factory.mover_id(),
            length=random.randint(1, max_length),
            top_left_coordinate=None
        )
        print(mover)
        return mover

    @staticmethod
    def build_vertical_mover_list(max_length: int, count: int) -> List[HorizontalMover]:
        return [EntityFactory.build_vertical_mover(max_length) for _ in range(count)]


    @staticmethod
    def build_board(
            dimension=Dimension(21, 21),
            max_entity_dimension: int = 7,
            max_entities: int = 10
    ) -> 'Board':
        board = Board()
        board.add_horizontal_mover(EntityFactory.horizontal_mover(max_height=max_entity_dimension))
        return board


