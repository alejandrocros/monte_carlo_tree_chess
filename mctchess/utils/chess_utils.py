import random

from chess import Board


def random_move(board):
    all_moves = [str(a) for a in list(board.legal_moves)]
    r_move = random.choice(all_moves)
    return r_move


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
        board = Board(fen="r1bqkbnr/p1pp1Qpp/1pn5/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4")
    return board
