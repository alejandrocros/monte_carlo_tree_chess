import random
from time import time
from typing import List

from chess import Board
from mctchess.game.game import Game
from mctchess.players import Player


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


def create_board(situation: str = "initial") -> Board:
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


def test_n_games(
    p1: Player, p2: Player, n_games: int, verbose: bool = False
) -> List[str]:
    t0 = time()
    results = list()
    for i in range(n_games):
        board = Board()
        game = (
            Game(p1, p2, board, verbose=verbose)
            if i % 2 == 0
            else Game(p2, p1, board, verbose=verbose)
        )
        game.play_game()
        outcome = board.outcome().winner
        if outcome is None:
            winner = "tie"
        elif i % 2 == 0 and outcome is True:
            winner = "p1"
        else:
            winner = "p2"
        if verbose and (i + 1) % 2 == 0:
            print(f"Finished with {i + 1} games in {(time() - t0) / 60:.3f} mins")
            print(
                f"Player 1: {results.count('p1')} Tied games: {results.count('tie')}\n"
            )
        results.append(winner)
    if verbose:
        print(f"Finished in {(time() - t0)/60:.3f} mins")
    return results
