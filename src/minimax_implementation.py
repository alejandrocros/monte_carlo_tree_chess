from src.utils.chess_utils import create_board
from src.players.minimax_player import MiniMaxPlayer

if __name__ == '__main__':
    print('Testing 3 different MiniMax players...')
    board = create_board('mate_in_one')
    player_1 = MiniMaxPlayer(depth=1)
    player_2 = MiniMaxPlayer(depth=2)
    player_3 = MiniMaxPlayer(depth=3)
    players = {"1": player_1, "2": player_2, "3": player_3}
    for key, player in players.items():
        move = player.play(board)
        print(f"Player {key} with depth={player.depth} chosed to play {move}")
