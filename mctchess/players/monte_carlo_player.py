import multiprocessing as mp
from hashlib import sha256
from numbers import Number
from random import shuffle
from time import time
from typing import Any, Tuple

import numpy as np
from chess import Board
from mctchess.players import Player
from mctchess.utils.chess_utils import get_random_move, parse_result


def rollout_move(
    board: Board, move: str, simulations: int = 10
) -> Tuple[str, Number[Any]]:
    rollouts_scores = list()
    for _ in range(simulations):
        child_node = board.copy()
        child_node.push(move)
        while not child_node.is_game_over():
            rand_move = get_random_move(child_node)
            child_node.push_san(rand_move)
        result = parse_result(child_node.result())
        rollouts_scores.append(result)
    return (move, np.mean(rollouts_scores))


def rollout(board: Board) -> float:
    while not board.is_game_over():
        move = get_random_move(board)
        board.push_san(move)
    result = parse_result(board.result())
    return result


class MCPlayer(Player):
    """
    Monte Carlo Player, following a policy based on pure Monte-Carlo simulations.
    :param n_simulations: number of simulations to run per move.
    :param no_pools: number of processes to use for parallelization.
    """

    def __init__(
        self, n_simulations: int = 10, no_pools: int = mp.cpu_count() - 1
    ) -> None:
        self.decription = self.describe()
        self.simulations = n_simulations
        self.no_pools = no_pools

    def play(self, board: Board) -> str:
        legal_moves = list(board.legal_moves)  # we shuffle for random choice

        if not legal_moves:
            return str()
        shuffle(legal_moves)

        no_pools = self.no_pools
        pool = mp.Pool(processes=no_pools)
        evaluations = pool.starmap(
            rollout_move, [(board, move, self.simulations) for move in legal_moves]
        )
        pool.close()

        evaluation_dict = {item[0]: item[1] for item in evaluations}
        if board.turn:  # white player
            best_move = max(evaluation_dict, key=evaluation_dict.get)
        else:
            best_move = min(evaluation_dict, key=evaluation_dict.get)
        return str(best_move)

    def describe(self) -> dict:
        timestamp = time()
        description = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "MCPlayer",
        }
        return description
