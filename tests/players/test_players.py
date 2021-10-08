import pytest
from chess import Board
from mctchess.players import Player
from mctchess.players.minimax_player import MiniMaxPlayer
from mctchess.players.random_player import RandomPlayer


@pytest.mark.parametrize("player_type", [("minimax-player"), ("random-player")])
def test_player_init(player_type):
    if player_type == "minimax-player":
        player = MiniMaxPlayer(depth=1)
    elif player_type == "random-player":
        player = RandomPlayer()
    description = player.describe()
    assert isinstance(description["id"], str)
    assert isinstance(description["name"], str)


@pytest.mark.parametrize("player_type", [("minimax-player"), ("random-player")])
def test_player_play(player_type):
    board = Board()
    if player_type == "minimax-player":
        player = MiniMaxPlayer(depth=1)
    elif player_type == "random-player":
        player = RandomPlayer()
    move = player.play(board)
    assert isinstance(move, str)
    assert move in [str(m) for m in list(board.legal_moves)]
