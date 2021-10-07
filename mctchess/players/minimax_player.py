import operator
from hashlib import sha256
from random import shuffle
from time import time
from typing import Tuple

import numpy as np
from chess import Board
from mctchess.players import Player
from mctchess.utils.evaluation import board_evaluation


def minimax(
    board: Board, depth: int = 2, add_mobility: bool = False
) -> Tuple[float, str]:
    player = 2 * int(board.turn) - 1  # 1 for white, -1 for black
    if depth == 0 or board.outcome() is not None:
        score = (
            board_evaluation(board, add_mobility)
            if not board.is_checkmate()
            else -player * np.inf
        )
        return score, str()
    else:
        final_eval = dict()
        player_function = max if player == 1 else min
        legal_moves = list(board.legal_moves)  # we shuffle for random choice
        shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            final_eval[str(move)] = minimax(
                board, depth=depth - 1, add_mobility=add_mobility
            )[0]
            board.pop()

        best_score = player_function(final_eval.items(), key=operator.itemgetter(1))[1]
        best_moves = [
            k for k, v in final_eval.items() if v == best_score
        ]  # we store all the moves with highest score
        best_move = best_moves[0]
        return best_score, best_move


def minimax_pruned(board: Board, depth: int = 2) -> Tuple[float, str]:
    def alpha_beta(board: Board, depth: int, alpha: float, beta: float) -> float:
        player = 2 * int(board.turn) - 1
        if depth == 0 or board.outcome() is not None:
            score = (
                board_evaluation(board)
                if not board.is_checkmate()
                else -player * np.inf
            )
            return score

        best_score = -player * np.inf
        legal_moves = list(board.legal_moves)
        shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            score = alpha_beta(board, depth - 1, alpha, beta)
            player_function = max if player == 1 else min
            best_score = player_function(best_score, score)
            alpha = max(alpha, best_score) if player == 1 else alpha
            beta = min(beta, best_score) if player != 1 else beta

            board.pop()
            if beta <= alpha:
                break
        return best_score

    player = 2 * int(board.turn) - 1
    global_score = -player * np.inf
    chosen_move = None

    for move in board.legal_moves:
        board.push(move)
        score = alpha_beta(board, depth - 1, -np.inf, np.inf)

        if (player == 1 and score > global_score) or (
            player == -1 and score < global_score
        ):
            global_score = score
            chosen_move = move

        board.pop()

    if chosen_move is None:  #  In case all moves are losing moves
        chosen_move = move

    return global_score, str(chosen_move)


class MiniMaxPlayer(Player):
    def __init__(
        self, depth: int = 2, add_mobility: bool = False, ab_pruning: bool = True
    ) -> None:
        self.depth = depth
        self.add_mobility = add_mobility
        self.ab_pruning = ab_pruning
        self.decription = self.describe()

    def play(self, board: Board) -> str:
        if self.ab_pruning:
            _, best_move = minimax_pruned(board=board, depth=self.depth)
        else:
            _, best_move = minimax(
                board=board, depth=self.depth, add_mobility=self.add_mobility
            )
        return best_move

    def describe(self) -> dict:
        timestamp = time()
        descr = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "MinMaxPlayer",
            "depth": self.depth,
            "add_mobility": self.add_mobility,
            "ab_pruning": self.ab_pruning,
        }
        return descr
