from abc import ABC, abstractmethod


class Portal(ABC):
    """Interface for obstacles that can be moved."""

    @abstractmethod
    def open(self):
        """changes the state of the portal to open."""
        pass

    @abstractmethod
    def close(self):
        """Change the state of the door to closed"""
        pass

    @abstractmethod
    def is_open(self) -> bool:
        """Returns True if the obstacle is allowed to travel to the given cells."""
        pass