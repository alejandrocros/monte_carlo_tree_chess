from abc import ABC, abstractmethod

from chess import Board


class Player(ABC):
    # Base class for all chess players
    def __init__(self):
        self.evaluations = dict()

    def update_history(self, board: Board, value: float) -> None:
        self.evaluations[board.board_fen()] = value

    @abstractmethod
    def play(self, board: Board) -> str:
        pass

    @abstractmethod
    def describe(self) -> dict:
        pass
