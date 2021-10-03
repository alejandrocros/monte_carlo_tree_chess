from abc import ABC, abstractmethod

from chess import Board


class Player(ABC):
    # Base class for all chess players
    @abstractmethod
    def play(board: Board) -> str:
        pass
