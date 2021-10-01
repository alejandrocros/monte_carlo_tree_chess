from src.players import Player
from chess import Board
import random


def get_random_move(board: Board) -> str:
    legal_moves = list(board.legal_moves)
    move = str(random.choice(legal_moves)) if legal_moves else str()
    return move


class RandomPlayer(Player):
    def play(self, board: Board) -> str:
        move = get_random_move(board)
        return move
