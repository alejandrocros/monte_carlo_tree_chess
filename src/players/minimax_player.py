import operator
import random
from typing import Tuple

import numpy as np
from chess import Board
from src.players import Player
from src.utils.evaluation import board_evaluation


def minimax(board: Board, depth: int=2) -> Tuple[float, str]:
    #  Recursive MiniMax function
    legal_moves = board.legal_moves
    player = 2 * int(board.turn) - 1 #  1 for white, -1 for black
    if depth==0 or board.is_checkmate():
        score = board_evaluation(board) if not board.is_checkmate() else -player * np.inf
        return score, str()
    else:
        final_eval = dict()
        player_function = max if player == 1 else min
        for move in legal_moves:
            child_node = board.copy()
            child_node.push_uci(str(move))
            final_eval[str(move)] = minimax(child_node, depth=depth-1)[0]

        best_score = player_function(final_eval.items(), key=operator.itemgetter(1))[1]
        best_moves = [k for k, v in final_eval.items() if v == best_score] #  we store all the moves with highest score
        best_move = random.choice(best_moves) #  random choice of move among best ones
        return best_score, best_move

class MiniMaxPlayer(Player):
    def __init__(self, depth=2):
        self.depth = depth

    def play(self, board: Board) -> str:
        best_move = minimax(board, self.depth)[1]
        return best_move
