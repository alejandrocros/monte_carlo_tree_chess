import random
from typing import Optional

from chess import Board

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
MAXLEGALMOVES = 200

def look(board, table):
    return table.get(board.h(), None)

def add(board, table):
    nplayouts = [0.0 for _ in range(MAXLEGALMOVES)]
    nwins = [0.0 for _ in range(MAXLEGALMOVES)]
    table[board.h()] = [1, nplayouts, nwins]

def create_board(situation='initial'):
    board = ChessBoard()
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

def random_move(board):
    all_moves = [str(a) for a in list(board.legal_moves)]
    r_move = random.choice(all_moves)
    return r_move

class ChessBoard(Board):
    def __init__(self, fen: Optional[str] = STARTING_FEN, *, chess960: bool = False):
        Board.__init__(self)

    def h(self):
        return self.board_fen()

    def playout(self, depth=0):
        """Set depth=0 to infinite-length exploration"""
        count = 0
        while(True and ((not depth) or count < depth)):
            moves = [str(a) for a in list(self.legal_moves)]
            if self.outcome():
                return self.score()
            n = random.randint(0, len(moves) - 1)
            self.play(moves[n])
            count += 1
        return self.score()

    def play(self, move):
        self.push_san(str(move))

    def score(self):
        _outcome = self.outcome()
        if _outcome is None:
            return 0.5
        result = _outcome.result()
        if result == '1-0':
            return 1.
        if result == '0-1':
            return 0.
        return 0.5

    def terminal(self):
        if self.score() == 0.5 and not self.outcome():
            return False
        return True
