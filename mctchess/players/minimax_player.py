import operator
from hashlib import sha256
from random import shuffle
from time import time
from typing import Callable, Tuple, Union

import numpy as np
from chess import Board
from mctchess.players import Player
from mctchess.utils.evaluation import board_evaluation


def minimax(evaluation_fn: Callable, board: Board, depth: int = 2) -> Tuple[float, str]:
    player = 2 * int(board.turn) - 1  # 1 for white, -1 for black
    if depth == 0 or board.outcome() is not None:
        score = evaluation_fn(board) if not board.is_checkmate() else -player * np.inf
        return score, str()
    else:
        final_eval = dict()
        player_function = max if player == 1 else min
        legal_moves = list(board.legal_moves)  # we shuffle for random choice
        shuffle(legal_moves)
        for move in legal_moves:
            board.push(move)
            final_eval[str(move)] = minimax(evaluation_fn, board, depth - 1)[0]
            board.pop()

        # best_move, best_score = player_function(
        #    final_eval.items(), key=operator.itemgetter(1))
        best_score = player_function(final_eval.items(), key=operator.itemgetter(1))[1]
        best_moves = [
            k for k, v in final_eval.items() if v == best_score
        ]  # we keep all the moves with highest score
        best_move = best_moves[0]
        return best_score, best_move


def minimax_pruned(
    evaluation_fn: Callable, board: Board, depth: int = 2
) -> Tuple[float, str]:
    def alpha_beta(board: Board, depth: int, alpha: float, beta: float) -> float:
        player = 2 * int(board.turn) - 1
        if depth == 0 or board.outcome() is not None:
            score = (
                evaluation_fn(board) if not board.is_checkmate() else -player * np.inf
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
    legal_moves = list(board.legal_moves)
    if len(legal_moves) == 0:
        return global_score, str()
    shuffle(legal_moves)
    for move in legal_moves:
        board.push(move)
        score = alpha_beta(board, depth - 1, -np.inf, np.inf)

        if (player == 1 and score > global_score) or (
            player == -1 and score < global_score
        ):
            global_score = score
            chosen_move = move

        board.pop()

    if chosen_move is None:
        #  In case all moves are losing moves it keeps the last one (random)
        chosen_move = move

    return global_score, str(chosen_move)


class MiniMaxPlayer(Player):
    def __init__(
        self, depth: int = 2, add_mobility: bool = False, ab_pruning: bool = True
    ) -> None:
        self.depth = depth
        self.add_mobility = add_mobility
        self.ab_pruning = ab_pruning
        self.player_logic = minimax if not self.ab_pruning else minimax_pruned
        self.decription = self.describe()
        self.evaluation_function = board_evaluation

    def evaluate(self, board: Board) -> float:
        return self.evaluation_function(board, self.add_mobility)

    def play(self, board: Board, debug: bool = False) -> Union[str, Tuple[float, str]]:
        best_score, best_move = self.player_logic(
            evaluation_fn=self.evaluate, board=board, depth=self.depth
        )
        if debug:
            return best_score, best_move
        return best_move

    def describe(self) -> dict:
        timestamp = time()
        description = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "MinMaxPlayer",
            "depth": self.depth,
            "add_mobility": self.add_mobility,
            "ab_pruning": self.ab_pruning,
        }
        return description
