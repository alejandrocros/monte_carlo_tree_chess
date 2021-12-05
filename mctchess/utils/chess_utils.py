import random

from chess import Board


def get_random_move(board: Board) -> str:
    legal_moves = list(board.legal_moves)
    move = str(random.choice(legal_moves)) if legal_moves else str()
    return move


def parse_result(result: str) -> float:
    if result == "1-0":
        return 1
    elif result == "0-1":
        return 0
    elif result == "1/2-1/2":
        return 0.5
    else:
        raise ValueError("Error: result not recognized")


def create_board(situation="initial"):
    board = Board()
    if situation == "one_move":
        board = Board(
            fen="r1bqkbnr/1pp1pQpp/p1np4/8/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        )
    elif situation == "mate_in_two":
        board = Board(
            fen="r1bqkbnr/1pp1p1pp/p1np4/8/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4"
        )
    elif situation == "mate_in_one":
        board = Board(
            fen="r1bqkbnr/p1pp1ppp/1pn5/4p3/2B1P3/5Q2/PPPP1PPP/RNB1K1NR w KQkq - 0 4"
        )
    elif situation == "mate_in_two_or_promote":
        board = Board(fen="8/3P2K1/p7/8/7R/6R1/1k6/8 w - - 0 1")
    elif situation == "capture_rook_loses":
        board = Board(fen="2r5/3r2k1/8/8/8/8/5PPP/2R3K1 w - - 0 1")
    elif situation == "ended_game":
        board = Board(
            fen="r1bqkbnr/p1pp1Qpp/1pn5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4"
        )
    return board
