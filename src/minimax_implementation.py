import operator
from typing import Dict, Tuple

import numpy as np
from chess import Board

from src.utils.chess_utils import create_board

VALUE_DICT = {
    "p": 100,
    "n": 350,
    "b": 350,
    "r": 525,
    "q": 1000,
    "k": 100000
}

def get_mobility(board: Board, mobility_coeff: float=1) -> float:
    player_legal_moves = len(list(board.legal_moves))
    _board = board.copy()
    _board.turn = not board.turn
    oponent_legal_moves = len(list(_board.legal_moves))
    return mobility_coeff * (player_legal_moves - oponent_legal_moves)

def board_evaluation(board: Board, add_mobility: bool=False) -> float:
    """
    Function for evaluating a chess position, given its board.
    It returns positive values for white evaluation.
    157 µs ± 1.87 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)"""
    score = float()
    fen = board.board_fen()
    for piece, value in VALUE_DICT.items():
        score += value * (fen.count(piece.upper()) - fen.count(piece))
    if add_mobility:
        mobility = get_mobility(board)
        if not board.turn:
            mobility *= -1
        score += mobility
    return score

def minimax(board: Board, depth: int=2) -> Tuple[float, str]:
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

        best_move = player_function(final_eval.items(), key=operator.itemgetter(1))[0]
        score = final_eval[best_move]
        return score, best_move

if __name__ == '__main__':
    board = create_board('mate_in_one')
    prueba1 = minimax(board, depth=1)
    prueba2 = minimax(board, depth=2)
    prueba3 = minimax(board, depth=3)
