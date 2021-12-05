from chess import Board
from mctchess.players import Player


class Game:
    def __init__(
        self, player_1: Player, player_2: Player, board: Board, verbose: bool = False
    ):
        self.white_player = player_1
        self.black_player = player_2
        self.board = board
        self.verbose = verbose
        self.game_history = list()

    def turn(self):
        return self.board.turn

    def compute_next_move(self):
        player = self.white_player if self.turn() else self.black_player
        move = player.play(self.board)
        return move

    def save_move_in_history(self, move):
        self.game_history.append(move)

    def execute_next_move(self):
        move = self.compute_next_move()
        self.board.push_san(move)
        self.save_move_in_history(move)

    def is_finished(self):
        return self.board.is_game_over()

    def play_n_moves(self, no_moves: int):
        for _ in range(no_moves):
            self.execute_next_move()

    def play_game(self):
        while not self.is_finished():
            self.execute_next_move()
            if self.verbose and self.board.ply() % 20 == 0:
                print(f"{self.board.ply()} turns played")

        if self.verbose:
            print(f"Game ended with result: {self.board.result()}")
