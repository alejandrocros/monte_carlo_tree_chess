import random
from hashlib import sha256
from time import time

from chess import Board
from mctchess.players import Player


def get_random_move(board: Board) -> str:
    legal_moves = list(board.legal_moves)
    move = str(random.choice(legal_moves)) if legal_moves else str()
    return move


class RandomPlayer(Player):
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
