"""The player class for the five in a row project"""

from typing import Union
import ChessGame
import gametree


class Player:
    """ A class for how two players move their pieces during the game
    """

    def make_move(self, game_state: ChessGame.ChessGame,
                  prev_move: Union[tuple[int, int], str]) -> None:
        """ Make move based on the previous move of opponent. The function will generate
        a gametree of depth 5, look for the subtree that has
        the highest score, and makes the move in game_state.
        """
        if prev_move == '*':
            game_state.make_move((7, 7))
        else:
            tree = gametree.GameTree(move=prev_move, black_move=game_state.get_is_black())
            tree.generate_tree_based_on_move(game_state, prev_move, 5)
            best_move = tree.get_max_score()
            game_state.make_move(best_move[0])
