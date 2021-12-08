from hashlib import sha256
from random import shuffle
from time import time
import multiprocessing as mp
from typing import List
import numpy as np
from chess import Board
from mctchess.players import Player
from mctchess.utils.chess_utils import get_random_move, parse_result


def rollout_move(board: Board, move, simulations=10) -> tuple:
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


class MCPlayer(Player):
    def __init__(self, n_simulations=10, no_pools=mp.cpu_count() - 1) -> None:
        self.decription = self.describe()
        self.simulations = n_simulations
        self.no_pools = no_pools

    def rollout(self, board: Board) -> float:
        while not board.is_game_over():
            move = get_random_move(board)
            board.push_san(move)
        result = parse_result(board.result())
        return result

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

        evaluations = {item[0]: item[1] for item in evaluations}
        if board.turn:  # white player
            best_move = max(evaluations, key=evaluations.get)
        else:
            best_move = min(evaluations, key=evaluations.get)
        return str(best_move)

    def describe(self) -> dict:
        timestamp = time()
        description = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "UctPlayer",
        }
        return description
