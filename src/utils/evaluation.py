from chess import Board

VALUE_DICT = {"p": 100, "n": 350, "b": 350, "r": 525, "q": 1000, "k": 100000}


def get_mobility(board: Board, mobility_coeff: float = 1) -> float:
    player_legal_moves = len(list(board.legal_moves))
    _board = board.copy()
    _board.turn = not board.turn
    oponent_legal_moves = len(list(_board.legal_moves))
    return mobility_coeff * (player_legal_moves - oponent_legal_moves)


def board_evaluation(board: Board, add_mobility: bool = False) -> float:
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
