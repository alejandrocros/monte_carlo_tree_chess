import argparse
import copy
import json
import math
import os
import random
from datetime import datetime
from time import time
from typing import Optional

import numpy as np
from chess import Board

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
MAXLEGALMOVES = 200


class NewBoard(Board):
    def __init__(self, fen: Optional[str] = STARTING_FEN, *, chess960: bool = False):
        Board.__init__(self)

    def h(self):
        return self.board_fen()

    def playout(self, depth=0):
        """Set depth=0 to infinite-length exploration"""
        count = 0
        while(True and ((not depth) or count < depth)):
            moves = self.legalMoves()
            if self.outcome():
                return self.score()
            n = random.randint(0, len(moves) - 1)
            self.play(moves[n])
            count += 1
        return self.score()

    def play(self, move):
        self.push_san(str(move))

    def legalMoves(self):
        return [str(a) for a in list(self.legal_moves)]

    def score(self):
        _outcome = self.outcome()
        if _outcome is None: return 0.5
        result = _outcome.result()
        if result == '1-0': return 1.
        if result == '0-1': return 0.
        return 0.5

    def terminal(self):
        if self.score() == 0.5 and not self.outcome():
            return False
        return True

def look(board):
    return Table.get(board.h(), None)

def add(board):
    nplayouts = [0.0 for _ in range(MAXLEGALMOVES)]
    nwins = [0.0 for _ in range(MAXLEGALMOVES)]
    Table[board.h()] = [1, nplayouts, nwins]

def create_board(situation='initial'):
    board = NewBoard()
    if situation == 'initial': return board
    board.push_san('g1f3')
    board.push_san('b8a6')
    board.push_san('f3g1')
    board.push_san('a6b8')
    board.push_san('e2e4')
    board.push_san('b8a6')
    board.push_san('d1f3')
    board.push_san('a6b8')
    board.push_san('f1c4')
    if situation == 'one_move':
        board.push_san('d7d6')
        board.push_san('f3f7')
    elif situation == 'mate_in_one':
        board.push_san('b8a6')
    return board

def UCT(board):
    if board.terminal():
        return board.score()
    t = look(board)
    if t != None:
        bestValue = -1000000.0
        best = 0
        moves = board.legalMoves()
        for i in range(0, len(moves)):
            val = 1000000.0
            #print(t)
            if t[1][i] > 0:
                Q = t[2][i] / t[1][i]
                if board.turn == False:
                    Q = 1 - Q
                val = Q + 0.4 * math.sqrt(math.log(t[0]) / t[1][i])
            if val > bestValue:
                bestValue = val
                best = i
        board.play(moves[best])
        res = UCT(board)
        t[0] += 1
        t[1][best] += 1
        t[2][best] += res
        return res
    else:
        add(board)
        return board.playout()

def BestMoveUCT(board, n):
    #Table = {}
    for i in range(n):
        #print('.', end='')
        b1 = copy.deepcopy(board)
        res = UCT(b1)
    t = look(board)
    moves = board.legalMoves()
    best = moves[0]
    bestValue = t[1][0]
    for i in range(1, len(moves)):
        if t[1][i] > bestValue:
            bestValue = t[1][i]
            best = moves[i]
    return best

def random_move(board):
    all_moves = list(board.legalMoves())
    r_move = random.choice(all_moves)
    return r_move

def save_array(filename, np_array):
    with open(filename, 'wb') as savefile:
        np.save(savefile, np_array)

def save_table(filename, table_dict):
    with open(filename, 'w+') as savefile:
        json.dump(table_dict, savefile)

def load_previous_table(previous_training_path):
    try:
        with open(previous_training_path, 'r+') as fp:
            Table = json.load(fp)
    except Exception as exc:
        print(f"Couldn't load the previous training due to {exc}")
        Table = dict()
    return Table

def print_stats(game, results, last_score):
    if results.shape[0] >= 10:
        print(f'Game {game + 1} --> {results.mean():.3f} | Table size: {len(Table.keys())} | Last result: {last_score} | 10-games mean: {results[-10:].mean()}')
    else:
        print(f'Game {game + 1} --> {results.mean():.3f} | Table size: {len(Table.keys())} | Last result: {last_score}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-nu", "--uct_iterations", help="n_iterations for uct", type=int, default=1)
    parser.add_argument("-ng", "--no_games", help="number of games for uct", type=int, default=4)
    parser.add_argument("-pt", "--previous_training", help="path to previous analysis", type=int, default=None)
    args = parser.parse_args()
    uct_iterations = args.uct_iterations
    number_of_games = args.no_games
    if args.previous_training is not None:
        Table = load_previous_table(args.previous_training)
    else:
        Table = dict()
    t0 = time()
    results = np.array(())
    last_score = None #to print the last score
    ts = datetime.now().strftime('%d%H%M%S')
    os.makedirs('./partial_results/', exist_ok=True)
    for game in range(number_of_games):
        print_stats(game, results, last_score)
        board = NewBoard()
        i = 1
        while not board.terminal():
            if i % 50 == 0:
                print(f'Move {i}        Elapsed time: {(time() - t0) / 60:.3f} mins')
            white_move = BestMoveUCT(board, n=uct_iterations)
            board.play(white_move)
            if board.turn:
                print('white')
                break
            try:
                black_move = random_move(board)
                board.play(black_move)
            except:#checkmate by white
                pass
            i += 1
        last_score = board.score()
        results = np.append(results, last_score)
        if game % 50 == 0:
            partial_results_file = f"./partial_results/tmp_results_{uct_iterations}_{game}_{ts}.npy"
            partial_table_file = f"./partial_results/tmp_table_{uct_iterations}_{ts}.json"
            save_array(partial_results_file, results)
            save_table(partial_table_file, Table)

    print(f'Mean of the results: {results.mean():.3f}')
    os.makedirs('./final_results/', exist_ok=True)
    final_results_file = f"./final_results/results_{uct_iterations}_{game}_{ts}.npy"
    final_table_file = f"./final_results/table_{uct_iterations}_{game}_{ts}.json"
    save_array(final_results_file, results)
    save_table(final_table_file, Table)
