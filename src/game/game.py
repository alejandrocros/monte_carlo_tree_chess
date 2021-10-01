from chess import Board
from src.players import Player


class Game:
    def __init__(
        self, Player1: Player, Player2: Player, board: Board, verbose: bool = False
    ):
        self.white_player = Player1
        self.black_player = Player2
        self.board = board
        self.verbose = verbose

    def turn(self):
        return self.board.turn

    def compute_next_move(self):
        player = self.white_player if self.turn else self.black_player
        move = player.play(self.board)
        return move

    def execute_next_move(self):
        move = self.compute_next_move()
        self.board.push_san(move)

    def is_finished(self):
        return self.board.is_checkmate()

    def play_n_moves(self, no_moves: int):
        for _ in range(no_moves):
            self.execute_next_move()

    def play_game(self):
        while not self.is_finished():
            self.execute_next_move()

        if self.verbose:
            print(f"Game ended with result: {self.board.result()}")
