import sys
from pathlib import Path

import pygame

from geometry import Dimension, GridCoordinate
from board import Board

from grid_entity import DiagonalMover, VerticalMover

from game_display import GameDisplay
from id_factory import id_factory

sys.path.append(str(Path(__file__).parent.absolute()))

def main():
    board = Board(dimension=Dimension(length=8, height=8))

    board.add_new_entity(GridCoordinate(7,0), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,1), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,2), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,3), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,4), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,5), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(7,7), VerticalMover(mover_id=id_factory.mover_id(), length=1))

    board.add_new_entity(GridCoordinate(6,0), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,1), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,2), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,3), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,4), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,5), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,6), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(6,7), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))

    board.add_new_entity(GridCoordinate(0,0), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,1), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,2), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,3), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,4), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,5), VerticalMover(mover_id=id_factory.mover_id(), length=1))
    board.add_new_entity(GridCoordinate(0,7), VerticalMover(mover_id=id_factory.mover_id(), length=1))

    board.add_new_entity(GridCoordinate(1,0), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,1), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,2), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,3), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,4), DiagonalMover(mover_id=id_factory.mover_id(), dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,5), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,6), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))
    board.add_new_entity(GridCoordinate(1,7), DiagonalMover(mover_id=id_factory.mover_id(),  dimension=Dimension(length=1, height=1)))

    visualizer = GameDisplay(board)
    # visualizer.board.add_new_entity(GridCoordinate(5, 0), DiagonalMover(mover_id=id_factory.mover_id(), dimension=4))


    clock = pygame.time.Clock()
    frame_count = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                visualizer.handle_mouse_down(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                visualizer.handle_mouse_up(event)
            elif event.type == pygame.MOUSEMOTION:
                visualizer.handle_mouse_motion(event)

        visualizer.update_display()
        clock.tick(200)
        frame_count += 1
        if frame_count % 60== 0:
            print(f"Frame {frame_count}")
    visualizer.close()

if __name__ == "__main__":
    main()