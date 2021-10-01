import argparse
import copy
import math
import os
from datetime import datetime
from time import time

import numpy as np

from src.board_functions import ChessBoard, addAMAF, look, random_move
from src.logger import print_stats
from src.utils.general_utils import load_previous_table, save_array, save_table
from src.uct_iterated import best_move_uct


def playout_AMAF(board, played):
    while True:
        moves = []
        moves = [str(a) for a in list(board.legal_moves)]
        if len(moves) == 0 or board.terminal():
            return board.score()
        n = random.randint(0, len(moves) - 1)
        played.append(moves[n].code(self))
        board.play(moves[n])


def rave(board, played):
    if board.terminal():
        return board.score()
    t = look(board)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = [str(a) for a in list(board.legal_moves)]
        bestcode = moves[0].code(board)
        for i in range(0, len(moves)):
            val = 1000000.0
            code = moves[i].code(board)
            if t[3][code] > 0:
                beta = t[3][code] / (t[1][i] + t[3][code] + 1e-5 * t[1][i] * t[3][code])
                Q = 1
                if t[1][i] > 0:
                    Q = t[2][i] / t[1][i]
                    if board.turn is False:
                        Q = 1 - Q
                AMAF = t[4][code] / t[3][code]
                if board.turn is False:
                    AMAF = 1 - AMAF
                val = (1.0 - beta) * Q + beta * AMAF
            if val > bestValue:
                bestValue = val
                best = i
                bestcode = code
        board.play(moves[best])
        res = rave(board, played)
        t[0] += 1
        t[1][best] += 1
        t[2][best] += res
        played.insert(0, bestcode)
        for k in range(len(played)):
            code = played[k]
            seen = False
            for j in range(k):
                if played[j] == code:
                    seen = True
            if not seen:
                t[3][code] += 1
                t[4][code] += res
        return res
    else:
        table = addAMAF(board)
        return playout_AMAF(board, played)


def best_move_rave(board, n):
    for i in range(n):
        b1 = copy.deepcopy(board)
        res = rave(b1, [])
    t = look(board)
    moves = [str(a) for a in list(board.legal_moves)]
    best = moves[0]
    bestValue = t[1][0]
    for i in range(1, len(moves)):
        if t[1][i] > bestValue:
            bestValue = t[1][i]
            best = moves[i]
    return best


PLAYERS = {"uct": best_move_uct, "random": random_move, "rave": best_move_rave}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-nu", "--uct_iterations", help="n_iterations for uct", type=int, default=5
    )
    parser.add_argument(
        "-ng", "--no_games", help="number of games for uct", type=int, default=5
    )
    parser.add_argument(
        "-pt",
        "--previous_training",
        help="path to previous analysis",
        type=int,
        default=None,
    )
    parser.add_argument(
        "-s",
        "--save_results",
        help="wether to save the results or not",
        type=bool,
        default=False,
    )
    parser.add_argument(
        "-p1", "--player_1", help="algorithm used by player 1", type=str, default="rave"
    )
    parser.add_argument(
        "-p2",
        "--player_2",
        help="algorithm used by player 2",
        type=str,
        default="random",
    )

    args = parser.parse_args()
    uct_iters = args.uct_iterations

    number_of_games = args.no_games
    if args.previous_training is not None:
        table = load_previous_table(args.previous_training)
    else:
        table = dict()
    table2 = dict()

    player_1 = PLAYERS.get(args.player_1, PLAYERS["uct"])
    player_2 = PLAYERS.get(args.player_2, PLAYERS["uct"])

    t0 = time()
    results = np.array(())
    last_score = None  # to print the last score in the 1st iteration
    ts = datetime.now().strftime("%d%H%M%S")

    SAVE_RESULTS = args.save_results
    if SAVE_RESULTS:
        os.makedirs("../partial_results/", exist_ok=True)
        os.makedirs("../final_results/", exist_ok=True)

    player_1_white = True
    for game in range(number_of_games):
        print_stats(game, results, last_score, table1=table, table2=table2)
        board = ChessBoard()
        i = 1
        while not board.terminal():
            if i % 50 == 0:
                print(f"Move {i}        Elapsed time: {(time() - t0) / 60:.3f} mins")

            if player_1_white:
                white_move = player_1(board, n=uct_iters, table=table)
                board.play(white_move)
                if not board.terminal():
                    black_move = player_2(
                        board, n=uct_iters, table=table2, c_utc=math.sqrt(2)
                    )
                    board.play(black_move)
            else:
                white_move = player_2(
                    board, n=uct_iters, table=table2, c_utc=math.sqrt(2)
                )
                board.play(white_move)
                if not board.terminal():
                    black_move = player_1(board, n=uct_iters, table=table)
                    board.play(black_move)

            i += 1
        last_score = board.score() if player_1_white else 1 - board.score()
        results = np.append(results, last_score)
        if game % 50 == 0 and SAVE_RESULTS:
            partial_results_file = (
                f"../partial_results/tmp_results_{uct_iters}_{game}_{ts}.npy"
            )
            partial_table_file = f"../partial_results/tmp_table_{uct_iters}_{ts}.json"
            save_array(partial_results_file, results)
            save_table(partial_table_file, table)

        player_1_white = not player_1_white

    print(f"Mean of the results: {results.mean():.3f}")

    if SAVE_RESULTS:
        final_results_file = f"../final_results/results_{uct_iters}_{game}_{ts}.npy"
        final_table_file = f"../final_results/table_{uct_iters}_{game}_{ts}.json"
        save_array(final_results_file, results)
        save_table(final_table_file, table)
