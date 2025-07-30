# First, define your custom exceptions (in a separate exceptions.py file)
class GameError(Exception):
    """Base exception for all src-related errors"""
    pass

class InvalidBoardError(GameError):
    """Raised when the board is not valid"""
    pass

class InvalidNumberOfRowsError(GameError):
    """Raised when the number of rows is not valid"""
    pass

class InvalidNumberOfColumnsError(GameError):
    """Raised when the number of columns is not valid"""
    pass

class InvalidIdError(GameError):
    """Raised when an mover_id_counter iss not valid for the src"""
    pass

class InvalidFigureHeightError(GameError):
    """Raised when a occupant's height is not valid"""
    pass

class InvalidFigureLengthError(GameError):
    """Raised when a occupant's height is not valid"""
    pass

class FigureAreaBelowLimitError(GameError):
    """Raised when a occupant's area is below the limit"""

class InvalidIdError(GameError):
    """Raised when an mover_id_counter iss not valid for the src"""
    pass

class InvalidSquareError(GameError):
    """Raised when attempting to interact with an invalid cell"""
    pass

class NullSquareEntryError(GameError):
    """Raised when attempting to enter a cell that does not exist"""
    pass

class OccupiedSquareEntryError(GameError):
    """Raised when attempting to enter an already occupied cell"""
    pass

class SquareNotVacatedError(GameError):
    """Raised when attempting to leave a cell that is not vacated"""

class SelfOccupiedSquareError(GameError):
    """Raised when attempting to enter a cell already occupied by self"""
    pass

class SquareOwnershipError(GameError):
    """Raised when attempting to leave a cell owned by a different occupant."""
    pass

class NoSquareToLeaveError(GameError):
    """Raised when attempting to leave a cell while not occupying any"""
    pass

class NegativeRowError(GameError):
    """Raised Cell cannot be on a negative row."""
    pass

class NegativeColumnError(GameError):
    """Cell cannot be on a negative column."""
    pass
