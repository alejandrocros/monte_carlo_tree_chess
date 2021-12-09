from hashlib import sha256
from time import time

from chess import Board
from mctchess.players import Player
from mctchess.utils.chess_utils import get_random_move


class RandomPlayer(Player):
    """
    A player with a random-move policy.
    """

    def __init__(self) -> None:
        self.decription = self.describe()

    def play(self, board: Board) -> str:
        move = get_random_move(board)
        return move

    def describe(self) -> dict:
        timestamp = time()
        descr = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "RandomPlayer",
        }
        return descr
