import pytest
from chess import Board
from mctchess.utils.chess_utils import create_board
from mctchess.players.minimax_player import MiniMaxPlayer
from mctchess.players.random_player import RandomPlayer
from mctchess.players.monte_carlo_player import MCPlayer


def get_player(player_type):
    if player_type == "minimax-pruned":
        return MiniMaxPlayer(depth=1, add_mobility=False, ab_pruning=True)
    elif player_type == "minimax-not-pruned":
        return MiniMaxPlayer(depth=1, add_mobility=False, ab_pruning=False)
    elif player_type == "monte-carlo":
        return MCPlayer(n_simulations=1, no_pools=1)
    elif player_type == "random":
        return RandomPlayer()
    else:
        raise ValueError("Invalid player type")


@pytest.mark.parametrize(
    "player_type", [("minimax-pruned"), ("minimax-not-pruned"), ("monte-carlo"), ("random")]
)
def test_player_init(player_type):
    player = get_player(player_type)
    description = player.describe()
    assert isinstance(description["id"], str)
    assert isinstance(description["name"], str)


@pytest.mark.parametrize(
    "player_type", [("minimax-pruned"), ("minimax-not-pruned"), ("monte-carlo"), ("random")]
)
def test_player_play(player_type):
    board = Board()
    player = get_player(player_type)
    move = player.play(board)
    assert isinstance(move, str)
    assert move in [str(m) for m in list(board.legal_moves)]  #  Check if move is legal


@pytest.mark.parametrize(
    "player_type", [("minimax-pruned"), ("minimax-not-pruned"), ("monte-carlo"), ("random")]
)
def test_player_play_ended_game(player_type):
    board = create_board("ended_game")
    player = get_player(player_type)
    move = player.play(board)
    assert move == str()
