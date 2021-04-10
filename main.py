"""The file that run the game."""

from Player import NormalPlayer, IntelligentPlayer
from ChessGame import ChessGame
from Gametree import GameTree
import math
import pprint


def run_game_eve(visualization: bool = False) -> None:
    """run a EVE chess game.
    """
    game = ChessGame()
    normal_player = NormalPlayer('white', game)
    intelligent_player = IntelligentPlayer('black', game)
    cur_player = 'black'
    cur = intelligent_player

    score = None
    i = 0
    while score != math.inf and score != math.inf * -1 and i < 26:
        i += 1
        if game.prev_move is None:
            move = (7, 7)
            game.make_move(move)
            game.prev_move = move
            cur_player = 'white'
            cur = normal_player
            score = game.get_score()
            print(f"Current score is {score}.")
            continue

        move = cur.choose_move()
        # TODO:
        print(game.get_valid_moves())
        game.make_move(move)
        print(cur_player)
        game.prev_move = move

        if cur_player == 'black':
            cur_player = 'white'
            cur = normal_player
        else:
            cur_player = 'black'
            cur = intelligent_player

        # Check is the game is over.
        score = game.get_score()
        print(f"Current score is {score}.")

        game.print_board()

    # board = game._board
    # x = []
    # for _ in range(15):
    #     x.append([])
    # for i in range(len(board)):
    #     for j in range(len(board[i])):
    #         x[i].append(board[i][j])

    # for i in range(15):
    #     print(x[i])
    game.print_board()
    print(game.prev_move)

    if score == math.inf:
        # black wins.
        print("Intelligent player(black) wins.")
    elif score == math.inf * -1:
        # white wins.
        print("Normal player (white) wins.")
    else:
        print("It's a draw!")


# def run_game_pve(visualization: bool = True) -> None
#     """run the game of human versus AI.
#     """
#     game = ChessGame()
#     ai_player = IntelligentPlayer('black', game)
#     cur_player = 'black'
#     score = None
#     while score != math.inf and score != math.inf * -1:
#         move = ai_player.choose_move()

if __name__ == '__main__':
    run_game_eve()
