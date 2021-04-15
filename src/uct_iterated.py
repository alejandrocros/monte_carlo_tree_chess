import argparse
import copy
import math
import os
from datetime import datetime
from time import time

import numpy as np

from board_functions import ChessBoard, add, look, random_move
from logger import print_stats
from utils import load_previous_table, save_array, save_table


def UCT(board, table):
    if board.terminal():
        return board.score()
    t = look(board, table=table)
    if t is not None:
        bestValue = -1000000.0
        best = 0
        moves = [str(a) for a in list(board.legal_moves)]
        for i in range(0, len(moves)):
            val = 1000000.0
            if t[1][i] > 0:
                Q = t[2][i] / t[1][i]
                if board.turn == False:
                    Q = 1 - Q
                val = Q + 0.4 * math.sqrt(math.log(t[0]) / t[1][i])
            if val > bestValue:
                bestValue = val
                best = i
        board.play(moves[best])
        res = UCT(board, table=table)
        t[0] += 1
        t[1][best] += 1
        t[2][best] += res
        return res
    add(board, table=table)
    return board.playout()

def BestMoveUCT(board, n, table):
    for i in range(n):
        b1 = copy.deepcopy(board)
        res = UCT(b1, table=table)
    t = look(board, table=table)
    moves = [str(a) for a in list(board.legal_moves)]
    best = moves[0]
    bestValue = t[1][0]
    for i in range(1, len(moves)):
        if t[1][i] > bestValue:
            bestValue = t[1][i]
            best = moves[i]
    return best

PLAYERS = {"uct": BestMoveUCT, "random": random_move}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-nu", "--uct_iterations", help="n_iterations for uct",
                        type=int, default=5)
    parser.add_argument("-ng", "--no_games", help="number of games for uct",
                        type=int, default=5)
    parser.add_argument("-pt", "--previous_training", help="path to previous analysis",
                        type=int, default=None)
    parser.add_argument("-s", "--save_results", help="wether to save the results or not",
                        type=bool, default=False)
    parser.add_argument("-p1", "--player_1", help="algorithm used by player 1",
                        type=str, default='uct')
    parser.add_argument("-p2", "--player_2", help="algorithm used by player 2",
                        type=str, default='random')

    args = parser.parse_args()
    uct_iters = args.uct_iterations

    number_of_games = args.no_games
    if args.previous_training is not None:
        table = load_previous_table(args.previous_training)
    else:
        table = dict()

    player_1 = PLAYERS.get(args.player_1, PLAYERS["uct"])
    player_2 = PLAYERS.get(args.player_2, PLAYERS["random"])

    t0 = time()
    results = np.array(())
    last_score = None  #to print the last score
    ts = datetime.now().strftime('%d%H%M%S')

    SAVE_RESULTS = args.save_results
    if SAVE_RESULTS:
        os.makedirs('../partial_results/', exist_ok=True)
        os.makedirs('../final_results/', exist_ok=True)

    for game in range(number_of_games):
        print_stats(game, results, last_score, table)
        board = ChessBoard()
        i = 1
        while not board.terminal():
            if i % 50 == 0:
                print(f'Move {i}        Elapsed time: {(time() - t0) / 60:.3f} mins')
            white_move = player_1(board, n=uct_iters, table=table)
            board.play(white_move)
            if board.turn:
                print('white')
                break
            try:
                black_move = player_2(board)
                board.play(black_move)
            except:  #checkmate by white
                pass
            i += 1
        last_score = board.score()
        results = np.append(results, last_score)
        if game % 50 == 0 and SAVE_RESULTS:
            partial_results_file = f"../partial_results/tmp_results_{uct_iters}_{game}_{ts}.npy"
            partial_table_file = f"../partial_results/tmp_table_{uct_iters}_{ts}.json"
            save_array(partial_results_file, results)
            save_table(partial_table_file, table)

    print(f'Mean of the results: {results.mean():.3f}')

    if SAVE_RESULTS:
        final_results_file = f"../final_results/results_{uct_iters}_{game}_{ts}.npy"
        final_table_file = f"../final_results/table_{uct_iters}_{game}_{ts}.json"
        save_array(final_results_file, results)
        save_table(final_table_file, table)
