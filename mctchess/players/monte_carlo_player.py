from hashlib import sha256
from random import shuffle
from time import time

import numpy as np
from chess import Board
from mctchess.players import Player
from mctchess.utils.chess_utils import get_random_move, parse_result


class MCPlayer(Player):
    def __init__(self, simulations=10) -> None:
        self.decription = self.describe()
        self.simulations = simulations
        self.history = dict()  # {board_position: {"ratio": 0.22, "visits": 2}}

    def rollout(self, board: Board) -> float:
        while not board.is_game_over():
            move = get_random_move(board)
            board.push_san(move)
        result = parse_result(board.result())
        return result

    def play(self, board: Board) -> str:
        legal_moves = list(board.legal_moves)  # we shuffle for random choice
        shuffle(legal_moves)
        evaluations = dict()
        for move in legal_moves:
            rollouts_scores = list()
            for _ in range(self.simulations):
                child_node = board.copy()
                child_node.push(move)
                rollout = self.rollout(child_node)
                rollouts_scores.append(rollout)
            mean_score = np.mean(rollouts_scores)
            evaluations[move] = mean_score
        if board.turn:  # white player
            best_move = max(evaluations, key=evaluations.get)
        else:
            best_move = min(evaluations, key=evaluations.get)
        return best_move

    def describe(self) -> dict:
        timestamp = time()
        description = {
            "id": sha256(str(timestamp).encode("utf-8")).hexdigest(),
            "name": "UctPlayer",
        }
        return description
